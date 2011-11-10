#!/usr/bin/env python

# Gnome Tray Services - For Ubuntu and Debian Distros
# A simple application to help start and stop services from the tray.

# Sami Khan, Etopian Inc. http://www.etopian.com
# Start and shutdown init.d services.
# GPL Version 3 - http://www.fsf.org/licensing/licenses/gpl-3.0.html
# AppIndicator by Edder Rojas http://paindev.wordpress.com

# Todo:
# - Scan for running services each time the menu opens, so if services are
# started manually from the console, it knows about them.
# - Make a dialog for adding/removing any init.d service from the menu.s
# - Perhaps wrap the Services into a Class.

# Configure services
services = ['apache2',
           ['mysql', '/var/run/mysqld/mysqld.pid']]
           # 'memcached',
           #['cups', '/var/run/cups/cupsd.pid'],
           #['mpd', '/var/run/mpd/pid'],
#            'gpsd',
#            'bluetooth',
           #['bind9', '/var/run/bind/run/named.pid']]

# === Don't edit below here, unless you know what you are doing! ===

import gtk
import pygtk
import subprocess
import os.path
import time
import appindicator
import pynotify
from types import *

class TrayServicesIndicator:

	#available services
	services = ['apache2',
			   ['mysql', '/var/run/mysqld/mysqld.sock']]

	# class constructor
	def __init__(self):
		self.ind = appindicator.Indicator(
				       "example-simple-client",
				       "gnome-do-symbolic",
				       appindicator.CATEGORY_APPLICATION_STATUS)

		self.ind.set_status(appindicator.STATUS_ACTIVE)
		self.ind.set_attention_icon("gnome-do-symbolic")

		#create a menu
		self.menu = gtk.Menu()

		for service in self.services:
			if(type(service) is ListType):
				service_name = service[0]
				service_pid_file = service[1]
			else:
				service_name = service

			if(self.service_is_running(service)):
				self.menu.append(self.service_menu_item_create(service, service_name, self.menu, 'stop'))
			else:
				self.menu.append(self.service_menu_item_create(service, service_name, self.menu, 'start'))
		#menu separator
		#menuItem = gtk.SeparatorMenuItem()
		#self.menu.append(menuItem)
		#menuItem.show()

		# quit menu
		#menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
		#menuItem.connect('activate', self.quit_cb, self.menu)
		#menuItem.show()
		#self.menu.append(menuItem)

		self.ind.set_menu(self.menu)

	# quit application by menu
	def quit_cb(self, widget, data = None):
		if data:
			data.set_visible(False)
		gtk.main_quit()

	# run a notification
	def notify(self, service, msg):
		n = pynotify.Notification(service+" "+msg)
		n.show()

	# call to status change
	def service_change_state(self, path, op):
		subprocess.call(['gksudo','--description','Tray Indicator Services','/etc/init.d/'+path, op])

	# Check if the process is running
	def service_is_running(self, service):
		if(type(service) is ListType):
			service_pid_path = service[1]
			if (os.path.exists(service_pid_path)):
				return 1
		else:
			if(os.path.exists('/var/run/'+service+'.pid')):
				return 1
		return 0

	# alternate service widget base on his state
	def toggle_service(self, widget, service, service_name, menu, op):
		if(self.service_is_running(service)):
			self.service_change_state(service_name, 'stop')
			widget.set_active(False)
			self.notify(service_name, "not running")
		else:
			self.service_change_state(service_name, 'start')
			widget.set_active(True)
			self.notify(service_name, "running")

	# Create a menu item based on a process
	def service_menu_item_create(self, service, service_name, menu, op):
		menuItem = gtk.CheckMenuItem(service_name)
		if (self.service_is_running(service)):
			menuItem.set_active(True)
		else:
			menuItem.set_active(False)

		menuItem.connect("activate", self.toggle_service, service, service_name, menu, op)
		menuItem.show()

		return menuItem

# main gtk entry
def main():
	gtk.main()
	return 0

# application if runned directly
if __name__ == '__main__':
	trayServicesIndicator = TrayServicesIndicator()
	main()

