#!/usr/bin/with-contenv bashio

rm -rf /etc/services.d/zigbee2mqtt-*
COORDINATORS=$(bashio::config 'coordinators')
for COORDINATOR in $COORDINATORS
do
    NAME=$(echo $COORDINATOR | jq -r '.name')    
    CONFIG=$(echo $COORDINATOR | jq '.config')
    MQTT_SERVER=$(echo $CONFIG | jq -r '.mqtt.server')
    MQTT_USER=$(echo $CONFIG | jq -r '.mqtt.user')
    MQTT_PASSWORD=$(echo $CONFIG | jq -r '.mqtt.password')

    if ! bashio::services.available "mqtt" && [ "$MQTT_SERVER" == 'null' ]; then
        bashio::exit.nok "No internal MQTT service found and no MQTT server defined. Please install Mosquitto broker or specify your own."
    else
        bashio::log.info "MQTT available, fetching server detail ..."
        if [ "$MQTT_SERVER" == 'null' ]; then
            bashio::log.info "MQTT server settings not configured, trying to auto-discovering ..."
            MQTT_PREFIX="mqtt://"
            if [ $(bashio::services mqtt "ssl") = true ]; then
                MQTT_PREFIX="mqtts://"
            fi
            MQTT_SERVER="$MQTT_PREFIX$(bashio::services mqtt "host"):$(bashio::services mqtt "port")"
            bashio::log.info "Configuring '$MQTT_SERVER' mqtt server"
        fi
        if [ "$MQTT_USER" == 'null' ]; then
            bashio::log.info "MQTT credentials not configured, trying to auto-discovering ..."
            MQTT_USER=$(bashio::services mqtt "username")
            MQTT_PASSWORD=$(bashio::services mqtt "password")
            bashio::log.info "Configuring '$MQTT_USER' mqtt user"
        fi
    fi

    mkdir -p /config/zigbee2mqtt-multi-coordinator/$NAME
    echo "$CONFIG" | jq 'del(.data_path, .zigbee_shepherd_devices, .socat)' \
        | jq 'if .devices then .devices = (.devices | split(",")|map(gsub("\\s+";"";"g"))) else . end' \
        | jq 'if .groups then .groups = (.groups | split(",")|map(gsub("\\s+";"";"g"))) else . end' \
        | jq 'if .advanced.ext_pan_id_string then .advanced.ext_pan_id = (.advanced.ext_pan_id_string | (split(",")|map(tonumber))) | del(.advanced.ext_pan_id_string) else . end' \
        | jq 'if .advanced.network_key_string then .advanced.network_key = (.advanced.network_key_string | (split(",")|map(tonumber))) | del(.advanced.network_key_string) else . end' \
        | jq 'if .device_options_string then .device_options = (.device_options_string|fromjson) | del(.device_options_string) else . end' \
        | MQTT_USER="$MQTT_USER"  jq '.mqtt.user=env.MQTT_USER' \
        | MQTT_PASSWORD="$MQTT_PASSWORD" jq '.mqtt.password=env.MQTT_PASSWORD' \
        | MQTT_SERVER="$MQTT_SERVER" jq '.mqtt.server=env.MQTT_SERVER' \
        > /config/zigbee2mqtt-multi-coordinator/$NAME/configuration.yaml

    mkdir -p /etc/services.d/zigbee2mqtt-$NAME
    cp /etc/services.d/run.template /etc/services.d/zigbee2mqtt-$NAME/run
    sed -i "s/{{ data_path }}/\/config\/zigbee2mqtt-multi-coordinator\/$NAME/g" /etc/services.d/zigbee2mqtt-$NAME/run
    chmod +x /etc/services.d/zigbee2mqtt-$NAME/run
done
