#!/usr/bin/with-contenv bashio

COORDINATORS=$(bashio::config 'coordinators')
for COORDINATOR in $COORDINATORS
do
    NAME=$(echo $COORDINATOR | jq -r '.name')
    # TODO: support case when there is no frontend port in configuration
    PORT=$(echo $COORDINATOR | jq -r '.config.frontend.port')
    mkdir -p /etc/nginx/zigbee2mqtt
    cp /templates/proxy.conf.template /etc/nginx/zigbee2mqtt/$NAME.conf
    sed -i "s/{{ name }}/$NAME/g" /etc/nginx/zigbee2mqtt/$NAME.conf
    sed -i "s/{{ port }}/$PORT/g" /etc/nginx/zigbee2mqtt/$NAME.conf
done