import osmnx as ox

class OSM:
    def get_summary_of_area(self, address: str):
        tags = {
            'building': True,
            'amenity': True,
            'landuse': True,
            'highway': True
        }
        df = ox.features_from_address(address, tags, 500)
        amenities_summary = {}
        if 'amenity' in df.columns:
            amenities_summary = df['amenity'].dropna().value_counts().to_dict()

        building_summary = {}
        if 'building' in df.columns:
            building_summary = {k: v for k, v in df['building'].dropna().value_counts().to_dict().items() if k.lower() != 'yes'}

        landuse_summary = {}
        if 'landuse' in df.columns:
            landuse_summary = df['landuse'].dropna().value_counts().to_dict()

        return {
            "amenities": amenities_summary,
            "building_types": building_summary,
            "landuse": landuse_summary
        }
