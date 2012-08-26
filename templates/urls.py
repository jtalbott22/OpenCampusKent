#   Copyright 2011 OpenPlans and contributors
#
#   This file is part of OpenBlock
#
#   OpenBlock is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   OpenBlock is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with OpenBlock.  If not, see <http://www.gnu.org/licenses/>.
#

from django.conf.urls.defaults import *
from obadmin import admin
from ebpub.db import feeds, views

admin.autodiscover()

urlpatterns = patterns(

    '',
	# Add crime form, mgates14
	url(r'^addCrime/$', views.addCrime, name='ebpub-addCrime'),
    url(r'^policies/', views.policies, name='ebpub-policies'),
    url(r'^team/', views.team, name='ebpub-team'),
    (r'^admin/', include(admin.site.urls)),

    # ebpub provides all the UI for an openblock site.
    (r'^', include('ebpub.urls')),

)