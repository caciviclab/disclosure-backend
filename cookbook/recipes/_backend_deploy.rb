user 'backend'

directory '/data/backend' do
  recursive true
  owner 'backend'
  group 'backend'
end

file '/usr/local/bin/deploy-backend' do
  mode 0775
  group 'opencal'
end

file '/etc/init/disclosure-backend.conf' do
  source 'upstart.conf'
end

service 'disclosure-backend' do
  action [:enable, :start]
end
