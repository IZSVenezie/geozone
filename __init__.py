def classFactory(iface):
    from .plugin.GeoZone import GeoZone
    return GeoZone(iface)