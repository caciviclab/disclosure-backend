package 'nginx'

service 'nginx' do
  action [:enable, :start]
end

template '/etc/nginx/sites-available/disclosure-backend' do
  source 'nginx.conf.erb'

  notifies :reload, 'service[nginx]'
end

link '/etc/nginx/sites-enabled/disclosure-backend' do
  to '/etc/nginx/sites-available/disclosure-backend'
end
