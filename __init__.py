def classFactory(iface):
    from .plugin.GeoZONE import GeoZONE
    return GeoZONE(iface)