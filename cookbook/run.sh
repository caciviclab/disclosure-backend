#!/usr/bin/env bash

echo 'Installing chef...'
ssh opencal.opendisclosure.io 'if [ ! $(which chef-solo) ]; then curl -L https://www.chef.io/chef/install.sh | sudo bash; fi'

echo 'Installing /etc/chef/solo.rb'
cat <<EOF | ssh opencal.opendisclosure.io 'sudo mkdir -p /etc/chef && sudo tee /etc/chef/solo.rb >/dev/null'
cookbook_path "/tmp/disclosure-backend"
json_attribs "/etc/chef/solo.json"
EOF

echo 'Installing /etc/chef/solo.json'
echo '{ "run_list": "recipe[disclosure-backend]" }' | ssh opencal.opendisclosure.io 'sudo tee /etc/chef/solo.json >/dev/null'

echo 'Deploying...'
rsync -r ../cookbook opencal.opendisclosure.io:/tmp/disclosure-backend/
ssh opencal.opendisclosure.io '
rm -rf /tmp/disclosure-backend/disclosure-backend &&
mv /tmp/disclosure-backend/cookbook /tmp/disclosure-backend/disclosure-backend &&
sudo chef-solo
'
