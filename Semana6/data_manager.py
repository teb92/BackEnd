from database import SessionLocal
from models import User, Car, Address

class UserManager:
    def create_user(self, name, email):
        with SessionLocal() as session:
            user = User(name=name, email=email)
            session.add(user)
            session.commit()
            print("User created.")

    def update_user(self, user_id, name=None, email=None):
        with SessionLocal() as session:
            user = session.get(User, user_id)
            if user:
                if name:
                    user.name = name
                if email:
                    user.email = email
                session.commit()
                print("User updated.")
            else:
                print("User not found.")

    def delete_user(self, user_id):
        with SessionLocal() as session:
            user = session.get(User, user_id)
            if user:
                session.delete(user)
                session.commit()
                print("User deleted.")
            else:
                print("User not found.")

    def list_all_users(self):
        with SessionLocal() as session:
            users = session.query(User).all()
            for user in users:
                print(f"{user.id}: {user.name} ({user.email})")


# =======================
class CarManager:
    def create_car(self, brand, model, user_id=None):
        with SessionLocal() as session:
            car = Car(brand=brand, model=model, user_id=user_id)
            session.add(car)
            session.commit()
            print("Car created.")

    def update_car(self, car_id, brand=None, model=None, user_id=None):
        with SessionLocal() as session:
            car = session.get(Car, car_id)
            if car:
                if brand:
                    car.brand = brand
                if model:
                    car.model = model
                car.user_id = user_id  # can be None
                session.commit()
                print("Car updated.")
            else:
                print("Car not found.")

    def delete_car(self, car_id):
        with SessionLocal() as session:
            car = session.get(Car, car_id)
            if car:
                session.delete(car)
                session.commit()
                print("Car deleted.")
            else:
                print("Car not found.")

    def assign_car_to_user(self, car_id, user_id):
        with SessionLocal() as session:
            car = session.get(Car, car_id)
            user = session.get(User, user_id)
            if car and user:
                car.user_id = user.id
                session.commit()
                print("Car assigned to user.")
            else:
                print("Car or user not found.")

    def list_all_cars(self):
        with SessionLocal() as session:
            cars = session.query(Car).all()
            for car in cars:
                user_info = f"(User ID: {car.user_id})" if car.user_id else "(No user)"
                print(f"{car.id}: {car.brand} {car.model} {user_info}")


# =======================
class AddressManager:
    def create_address(self, street, city, user_id):
        with SessionLocal() as session:
            user = session.get(User, user_id)
            if not user:
                print("User not found. Cannot create address.")
                return
            address = Address(street=street, city=city, user_id=user_id)
            session.add(address)
            session.commit()
            print("Address created.")

    def update_address(self, address_id, street=None, city=None):
        with SessionLocal() as session:
            address = session.get(Address, address_id)
            if address:
                if street:
                    address.street = street
                if city:
                    address.city = city
                session.commit()
                print("Address updated.")
            else:
                print("Address not found.")

    def delete_address(self, address_id):
        with SessionLocal() as session:
            address = session.get(Address, address_id)
            if address:
                session.delete(address)
                session.commit()
                print("Address deleted.")
            else:
                print("Address not found.")

    def list_all_addresses(self):
        with SessionLocal() as session:
            addresses = session.query(Address).all()
            for address in addresses:
                print(f"{address.id}: {address.street}, {address.city} (User ID: {address.user_id})")