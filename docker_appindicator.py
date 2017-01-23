import os
import docker
import gi
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk # noqa
from gi.repository import AppIndicator3 as appindicator # noqa
import signal # noqa


APPINDICATOR_ID = 'docker_appindicator'

docker_client = docker.from_env()


def build_menu():
    menu = gtk.Menu()
    container_list = get_container_list()
    for container in container_list:
        menu_item = create_menu_item(container.name)
        menu.append(menu_item)
    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu


def create_menu_item(title):
    return gtk.MenuItem(title)


def get_container_list():
    return docker_client.containers.list()


def main():
    indicator = appindicator.Indicator.new(
        APPINDICATOR_ID,
        os.path.abspath('dockerlogo.svg'),
        appindicator.IndicatorCategory.SYSTEM_SERVICES
    )
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())

    # Default signal handler for Ctrl+c
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    # Main GTK loop
    gtk.main()


def quit(source):
    gtk.main_quit()


if __name__ == "__main__":
    main()
