package 'python-virtualenv'
package 'libmysqlclient-dev'
package 'libpq-dev'
package 'python-dev'

group 'opencal'

include_recipe 'disclosure-backend::_nginx'
include_recipe 'disclosure-backend::_backend_deploy'
