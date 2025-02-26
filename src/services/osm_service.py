import osmnx as ox
from geopandas import GeoDataFrame

class OSMService:
    def _get_feature_count(self, df: GeoDataFrame, col_name: str):
        if col_name in df.columns:
            return {k: v for k, v in df[col_name].dropna().value_counts().to_dict().items() if k.lower() != 'yes'}


    def get_features_near_address(self, address: str, radius_m: float = 500):
        tags = {
            'building': True,
            'amenity': True,
            'landuse': True
        }

        df = ox.features_from_address(address, tags, radius_m)

        amenity_count = self._get_feature_count(df, 'amenity')
        building_count = self._get_feature_count(df, 'building')
        landuse_count = self._get_feature_count(df, 'landuse')

        return {
            "amenity": amenity_count,
            "building": building_count,
            "landuse": landuse_count
        }
