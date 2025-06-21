from database import SessionLocal
from models import User, Car, Address


class UserManager:
    def __init__(self):
        self.session = SessionLocal()

    def create_user(self, name, email):
        user = User(name=name, email=email)
        self.session.add(user)
        self.session.commit()
        print("User created.")

    def update_user(self, user_id, name=None, email=None):
        user = self.session.get(User, user_id)
        if user:
            if name:
                user.name = name
            if email:
                user.email = email
            self.session.commit()
            print("User updated.")
        else:
            print("User not found.")

    def delete_user(self, user_id):
        user = self.session.get(User, user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
            print("User deleted.")
        else:
            print("User not found.")

    def list_all_users(self):
        users = self.session.query(User).all()
        for user in users:
            print(f"{user.id}: {user.name} ({user.email})")


class CarManager:
    def __init__(self):
        self.session = SessionLocal()

    def create_car(self, brand, model, user_id=None):
        car = Car(brand=brand, model=model, user_id=user_id)
        self.session.add(car)
        self.session.commit()
        print("Car created.")

    def update_car(self, car_id, brand=None, model=None, user_id=None):
        car = self.session.get(Car, car_id)
        if car:
            if brand:
                car.brand = brand
            if model:
                car.model = model
            if user_id is not None:  # allow setting to None
                car.user_id = user_id
            self.session.commit()
            print("Car updated.")
        else:
            print("Car not found.")

    def delete_car(self, car_id):
        car = self.session.get(Car, car_id)
        if car:
            self.session.delete(car)
            self.session.commit()
            print("Car deleted.")
        else:
            print("Car not found.")

    def assign_car_to_user(self, car_id, user_id):
        car = self.session.get(Car, car_id)
        user = self.session.get(User, user_id)
        if car and user:
            car.user_id = user.id
            self.session.commit()
            print("Car assigned to user.")
        else:
            print("Car or user not found.")

    def list_all_cars(self):
        cars = self.session.query(Car).all()
        for car in cars:
            user_info = f"(User ID: {car.user_id})" if car.user_id else "(No user)"
            print(f"{car.id}: {car.brand} {car.model} {user_info}")


class AddressManager:
    def __init__(self):
        self.session = SessionLocal()

    def create_address(self, street, city, user_id):
        user = self.session.get(User, user_id)
        if not user:
            print("User not found. Cannot create address.")
            return
        address = Address(street=street, city=city, user_id=user_id)
        self.session.add(address)
        self.session.commit()
        print("Address created.")

    def update_address(self, address_id, street=None, city=None):
        address = self.session.get(Address, address_id)
        if address:
            if street:
                address.street = street
            if city:
                address.city = city
            self.session.commit()
            print("Address updated.")
        else:
            print("Address not found.")

    def delete_address(self, address_id):
        address = self.session.get(Address, address_id)
        if address:
            self.session.delete(address)
            self.session.commit()
            print("Address deleted.")
        else:
            print("Address not found.")

    def list_all_addresses(self):
        addresses = self.session.query(Address).all()
        for address in addresses:
            print(f"{address.id}: {address.street}, {address.city} (User ID: {address.user_id})")