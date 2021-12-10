#!/usr/bin/with-contenv bashio
OPTIONS=$(cat /data/options.json)
for COORDINATOR in $(echo "${OPTIONS}" | jq -r '.coordinators[] | @base64' ); do
    DECODED_COORDINATOR=$(echo $COORDINATOR | base64 -d)
    NAME=$(echo $DECODED_COORDINATOR| jq -r .name)
    CONFIG=$(to_json.py "$(echo $DECODED_COORDINATOR | jq '.config')")
    # TODO: support case when there is no frontend port in configuration
    PORT=$(echo $CONFIG | jq '.frontend.port')
    mkdir -p /etc/nginx/zigbee2mqtt
    cp /templates/proxy.conf.template /etc/nginx/zigbee2mqtt/$NAME.conf
    sed -i "s/{{ name }}/$NAME/g" /etc/nginx/zigbee2mqtt/$NAME.conf
    sed -i "s/{{ port }}/$PORT/g" /etc/nginx/zigbee2mqtt/$NAME.conf
done