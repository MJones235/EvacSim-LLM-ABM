import osmnx as ox
from geopandas import GeoDataFrame
from shapely import Point
import hashlib
import json

from src.repositories.osm_repository import OSMRepository

class OSMService:
    osm_repository: OSMRepository

    def __init__(self):
        self.osm_repository = OSMRepository()

    def _get_feature_count(self, df: GeoDataFrame, col_name: str) -> dict:
        if col_name in df.columns:
            return {k: v for k, v in df[col_name].dropna().value_counts().to_dict().items() if k.lower() != 'yes'}
        return {}
    
    def _hash_query(self, address: str, radius_m: float) -> str:
        query_string = f"{address}_{radius_m}"
        return hashlib.sha256(query_string.encode()).hexdigest()

    def get_features_near_address(self, address: str, radius_m: float = 500):
        query_hash = self._hash_query(address, radius_m)
        cached_result = self.osm_repository.get_cached_response(query_hash)
        if cached_result:
            return json.loads(cached_result)

        tags = { 'building': True, 'amenity': True, 'landuse': True }

        df = ox.features_from_address(address, tags, radius_m)

        amenity_count = self._get_feature_count(df, 'amenity')
        building_count = self._get_feature_count(df, 'building')
        landuse_count = self._get_feature_count(df, 'landuse')

        features =  {
            "amenity": amenity_count,
            "building": building_count,
            "landuse": landuse_count
        }

        self.osm_repository.cache_response(query_hash, json.dumps(features))

        return features


    def get_feature_coordinates(self, address: str, radius_m: float, category: str, type: str, crs: str) -> Point:
        tags = {
            category: type
        }

        df = ox.features_from_address(address, tags, radius_m)
        df.geometry = df.geometry.to_crs(crs)
        random_feature = df.sample(n=1).iloc[0]
        return random_feature.geometry

