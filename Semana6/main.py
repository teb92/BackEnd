from data_manager import UserManager, CarManager, AddressManager
from models import Base
from database import engine

# 1. Ensure tables are created
Base.metadata.create_all(bind=engine)

# 2. Create managers
user_manager = UserManager()
car_manager = CarManager()
address_manager = AddressManager()

# === USERS ===
print("Creating user...")
user_manager.create_user("Alice", "alice@example.com")

print("Listing users:")
user_manager.list_all_users()

print("Updating user ID 1...")
user_manager.update_user(1, name="Alice Smith")

# === CARS ===
print("Creating car (not linked to user)...")
car_manager.create_car("Toyota", "Corolla")

print("Creating car for user ID 1...")
car_manager.create_car("Ford", "Mustang", user_id=1)

print("Assigning car ID 1 to user ID 1...")
car_manager.assign_car_to_user(1, user_id=1)

print("Listing cars:")
car_manager.list_all_cars()

# === ADDRESSES ===
print("Creating address for user ID 1...")
address_manager.create_address("123 Main St", "New York", user_id=1)

print("Listing addresses:")
address_manager.list_all_addresses()

