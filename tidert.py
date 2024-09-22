from typing import Dict, List, Type, Union


"""
    Represents an address in memory.

    Attributes:
        value (str): The address value as a string.
"""
class Address:
    def __init__(self, value):
        self.value = value 

    def __repr__(self) -> str:
        return f'{self.value}'
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Address):
            return self.value == other.value
        return False
    
    def __hash__(self) -> int:
        return hash(self.value)

    def __format__(self, format_spec: str) -> str:
        return format(f'{self.value}', format_spec)

    def get_memory_address(self) -> Type['Address']:
        return Address(f'{self.value[0]}0')

    def get_col_location(self)->int:
        return int(self.value[1])


"""
    Represents an instruction stored in memory.

    Attributes:
        value (str): The value of the instruction.
"""
class Instruction:
    def __init__(self, value: int):
        if len(value) != 4 or not value.isdigit():
            raise ValueError('Instruction must be a 4-digit decimal number.')
        self.value = value

    def __repr__(self) -> str:
        return self.value
    
    def __format__(self, format_spec: str) -> str:
        return format(f'{self.value}', format_spec)  


"""
    Represents a data value stored in memory.

    Attributes:
        value (str): The value of the data.
"""
class DataValue:
    def __init__(self, value):
        self.value = value

    def __repr__(self) -> str:
        return self.value
    
    def __format__(self, format_spec):
        return format(f'{self.value}', format_spec)
 

"""
    Represents the memory of the Simpletron, which can store instructions and data values.

    Attributes:
        memory (Dict[Address, List[Union[Instruction, DataValue]]]): 
            A dictionary mapping addresses to a list of instructions or data values.
"""
class Memory:
    memory: Dict[Address, List[Union[Instruction, DataValue]]] = {} 

    def __init__(self): pass
    
    @classmethod
    def initialize_memory(cls, num_locations: int) -> None:
        cls.memory = {Address(f'{i}0'): [] for i in range(num_locations)}
        for key in cls.memory:
            for _ in range(len(cls.memory)):
                cls.memory[key].append(Instruction('0000'))

    @classmethod
    def store_data(cls, address: Address, data: str) -> None:
        memory_address = address.get_memory_address() 

        if memory_address in cls.memory:
            loc = address.get_col_location()
            if 0 <= loc < len(cls.memory[memory_address]):
                cls.memory[memory_address][loc] = DataValue(data)
            else:
                raise IndexError("Column index out of range.")
        else:
            raise KeyError("Address not found in memory.")
        
    @classmethod
    def read_data(cls, address: Address) -> Union[Instruction, DataValue]:
        memory_address = address.get_memory_address() 
        loc = address.get_col_location()
        
        val = cls.memory[memory_address][loc]

        if not val:
            raise ValueError("No value found")

        return val; 

    @classmethod
    def dump(cls) -> None:
        for index in range(len(cls.memory)):
            print(f'{index:>10}', end=' ')
        print()

        for key in cls.memory:
            print(f'{key:>2}', end=' ')
            for loc in cls.memory[key]:
                content = '+' + f'{repr(loc)}' if isinstance(loc, Instruction) else repr(loc)
                print(f'{content:>10}', end=' ')
            print()


"""
    TEST 
"""

Memory.initialize_memory(10)

# Create Address objects
addr1 = Address('00')
addr2 = Address('45')   

# Store data in a specific address
Memory.store_data(addr1, 'hello')
Memory.store_data(addr2, 'world')

# Print memory
Memory.dump()

# Read data in a specific memory address
print(Memory.read_data(Address('45')))

