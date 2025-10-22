"""
Database Service Module
Handles MongoDB connection and basic database operations
"""

from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import logging
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseService:
    """
    MongoDB database service
    Provides connection management and common database operations
    """
    
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        """Singleton pattern to ensure single database connection"""
        if cls._instance is None:
            cls._instance = super(DatabaseService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize database service object without connecting yet.

        Connection to MongoDB is deferred until first use to avoid raising
        errors during module import (important in serverless environments).
        """
        # Do not attempt to connect here. Connection will be created lazily.
        return

    def _connect(self):
        """Establish connection to MongoDB and create indexes.

        This is called lazily when a database operation is attempted.
        """
        if self._client is not None:
            return

        try:
            # SSL/TLS configuration for Python 3.13+ compatibility
            self._client = MongoClient(
                Config.MONGODB_URI,
                serverSelectionTimeoutMS=5000,
                tlsAllowInvalidCertificates=True  # Allow invalid certificates for Python 3.13+
            )
            # Test connection
            self._client.admin.command('ping')
            self._db = self._client[Config.DATABASE_NAME]
            logger.info(f"Successfully connected to MongoDB: {Config.DATABASE_NAME}")
            self._create_indexes()
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            # Keep client as None so subsequent attempts can retry
            self._client = None
            self._db = None
            raise

    def _ensure_connection(self):
        """Ensure there is an active connection to the database.

        Call this at the start of any public DB method.
        """
        if self._client is None or self._db is None:
            self._connect()
    
    def _create_indexes(self):
        """
        Create database indexes for better query performance
        Called automatically during initialization
        """
        try:
            # Users collection indexes
            self._db.users.create_index([("username", ASCENDING)], unique=True)
            self._db.users.create_index([("email", ASCENDING)])
            
            # Courses collection indexes
            self._db.courses.create_index([("code", ASCENDING)])
            self._db.courses.create_index([("teacher_id", ASCENDING)])
            
            # Activities collection indexes
            self._db.activities.create_index([("course_id", ASCENDING)])
            self._db.activities.create_index([("teacher_id", ASCENDING)])
            self._db.activities.create_index([("link", ASCENDING)], unique=True)
            
            # Students collection indexes
            self._db.students.create_index([("course_id", ASCENDING)])
            self._db.students.create_index([("student_id", ASCENDING)])
            
            logger.info("Database indexes created successfully")
        except Exception as e:
            logger.error(f"Error creating indexes: {e}")
    
    @property
    def db(self):
        """Get database instance"""
        return self._db
    
    def get_collection(self, collection_name):
        """
        Get a specific collection from the database
        
        Args:
            collection_name (str): Name of the collection
            
        Returns:
            Collection: MongoDB collection object
        """
        # Ensure we have a connection before returning a collection
        self._ensure_connection()
        return self._db[collection_name]
    
    def insert_one(self, collection_name, document):
        """
        Insert a single document into a collection
        
        Args:
            collection_name (str): Name of the collection
            document (dict): Document to insert
            
        Returns:
            InsertOneResult: Result of the insert operation
        """
        try:
            self._ensure_connection()
            result = self._db[collection_name].insert_one(document)
            logger.info(f"Inserted document into {collection_name}: {result.inserted_id}")
            return result
        except Exception as e:
            logger.error(f"Error inserting document into {collection_name}: {e}")
            raise
    
    def find_one(self, collection_name, query):
        """
        Find a single document in a collection
        
        Args:
            collection_name (str): Name of the collection
            query (dict): Query filter
            
        Returns:
            dict: Found document or None
        """
        try:
            self._ensure_connection()
            return self._db[collection_name].find_one(query)
        except Exception as e:
            logger.error(f"Error finding document in {collection_name}: {e}")
            raise
    
    def find_many(self, collection_name, query, sort=None, limit=None):
        """
        Find multiple documents in a collection
        
        Args:
            collection_name (str): Name of the collection
            query (dict): Query filter
            sort (list): Sort specification
            limit (int): Maximum number of documents to return
            
        Returns:
            Cursor: MongoDB cursor with results
        """
        try:
            self._ensure_connection()
            cursor = self._db[collection_name].find(query)
            if sort:
                cursor = cursor.sort(sort)
            if limit:
                cursor = cursor.limit(limit)
            return list(cursor)
        except Exception as e:
            logger.error(f"Error finding documents in {collection_name}: {e}")
            raise
    
    def update_one(self, collection_name, query, update):
        """
        Update a single document in a collection
        
        Args:
            collection_name (str): Name of the collection
            query (dict): Query filter
            update (dict): Update operations
            
        Returns:
            UpdateResult: Result of the update operation
        """
        try:
            self._ensure_connection()
            result = self._db[collection_name].update_one(query, update)
            logger.info(f"Updated document in {collection_name}: {result.modified_count} modified")
            return result
        except Exception as e:
            logger.error(f"Error updating document in {collection_name}: {e}")
            raise
    
    def delete_one(self, collection_name, query):
        """
        Delete a single document from a collection
        
        Args:
            collection_name (str): Name of the collection
            query (dict): Query filter
            
        Returns:
            DeleteResult: Result of the delete operation
        """
        try:
            self._ensure_connection()
            result = self._db[collection_name].delete_one(query)
            logger.info(f"Deleted document from {collection_name}: {result.deleted_count} deleted")
            return result
        except Exception as e:
            logger.error(f"Error deleting document from {collection_name}: {e}")
            raise
    
    def count_documents(self, collection_name, query=None):
        """
        Count documents in a collection
        
        Args:
            collection_name (str): Name of the collection
            query (dict): Query filter (optional)
            
        Returns:
            int: Number of documents
        """
        try:
            self._ensure_connection()
            if query is None:
                query = {}
            return self._db[collection_name].count_documents(query)
        except Exception as e:
            logger.error(f"Error counting documents in {collection_name}: {e}")
            raise
    
    def close(self):
        """Close database connection"""
        if self._client:
            self._client.close()
            logger.info("Database connection closed")

# Create global database service instance
db_service = DatabaseService()
