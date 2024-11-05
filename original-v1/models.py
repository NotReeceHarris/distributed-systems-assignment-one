import uuid
from typing import Dict, Optional
import msgpack

class AdventurerClass:
    """
    Represents an adventurer with their core attributes and game-related statistics.
    
    Attributes:
        name (str): Name of the adventurer
        adventures_class (str): Character class type
        armour_class (int): Defensive rating
        level (int): Current experience level
        experience (int): Total accumulated experience
        take_damage_last_turn (bool): Flag indicating damage taken in previous turn
        hit_points (int): Current health points
    """
    
    def __init__(
        self, 
        name: str, 
        adventures_class: str, 
        armour_class: int, 
        level: int, 
        experience: int, 
        take_damage_last_turn: bool, 
        hit_points: int
    ):
        self.name = name
        self.adventures_class = adventures_class
        self.armour_class = armour_class
        self.level = level
        self.experience = experience
        self.take_damage_last_turn = take_damage_last_turn
        self.hit_points = hit_points
    
    def serialise(self) -> bytes:
        """
        Serialize the adventurer's data to a msgpack-encoded byte string.
        
        Returns:
            bytes: Msgpack-encoded representation of the adventurer's attributes
        """
        adventurer_data = {
            'name': self.name,
            'adventures_class': self.adventures_class,
            'armour_class': self.armour_class,
            'level': self.level,
            'experience': self.experience,
            'take_damage_last_turn': self.take_damage_last_turn,
            'hit_points': self.hit_points
        }
        
        return msgpack.packb(adventurer_data)
    
    @classmethod
    def deserialise(cls, serialized_data: bytes) -> 'AdventurerClass':
        """
        Deserialize msgpack-encoded byte data back into an AdventurerClass instance.
        
        Args:
            serialized_data (bytes): Msgpack-encoded adventurer data
        
        Returns:
            AdventurerClass: Reconstructed adventurer instance
        """
        data = msgpack.unpackb(serialized_data)
        return cls(**data)


class AdventurerStore:
    """
    A store for managing and serializing adventurer instances.
    
    Provides methods to add, retrieve, and serialize adventurers 
    using unique identifiers.
    """
    
    def __init__(self):
        """
        Initialize an empty adventurer store.
        """
        self._store: Dict[uuid.UUID, AdventurerClass] = {}
    
    def add(self, adventurer: AdventurerClass) -> uuid.UUID:
        """
        Add an adventurer to the store and generate a unique identifier.
        
        Args:
            adventurer (AdventurerClass): Adventurer to be added
        
        Returns:
            uuid.UUID: Unique identifier for the added adventurer
        """
        adventurer_id = uuid.uuid4()
        self._store[adventurer_id] = adventurer
        return adventurer_id
    
    def get(self, adventurer_id: uuid.UUID) -> Optional[AdventurerClass]:
        """
        Retrieve an adventurer by their unique identifier.
        
        Args:
            adventurer_id (uuid.UUID): Unique identifier of the adventurer
        
        Returns:
            Optional[AdventurerClass]: The adventurer if found, None otherwise
        """
        return self._store.get(adventurer_id)
    
    def serialise(self) -> bytes:
        """
        Serialize the entire adventurer store to a msgpack-encoded byte string.
        
        Returns:
            bytes: Msgpack-encoded representation of all adventurers
        """
        serialized_adventurers = {
            str(key): value.serialise() 
            for key, value in self._store.items()
        }

        print(serialized_adventurers)
        
        return msgpack.packb(serialized_adventurers)
    
    def deserialise(self, serialized_data: bytes) -> None:
        """
        Deserialize msgpack-encoded byte data and populate the store.
        
        Args:
            serialized_data (bytes): Msgpack-encoded adventurer store data
        """
        decoded_data = msgpack.unpackb(serialized_data)
        self._store.clear()
        
        for key, value in decoded_data.items():
            adventurer_id = uuid.UUID(hex=key)
            self._store[adventurer_id] = AdventurerClass.deserialise(value)