import streamlit as st
import sqlite3

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect("car_database.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            car_company TEXT,
            car_model TEXT,
            car_type TEXT,
            car_number TEXT,
            plate_number TEXT,
            kilometers_driven INTEGER,
            mileage REAL
        )
    """)
    conn.commit()
    conn.close()

# Add car data to the database
def add_car(car_company, car_model, car_type, car_number, plate_number, kilometers_driven, mileage):
    conn = sqlite3.connect("car_database.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO cars (car_company, car_model, car_type, car_number, plate_number, kilometers_driven, mileage)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (car_company, car_model, car_type, car_number, plate_number, kilometers_driven, mileage))
    conn.commit()
    conn.close()

# Fetch all car data from the database
def get_all_cars():
    conn = sqlite3.connect("car_database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM cars")
    data = c.fetchall()
    conn.close()
    return data

# Delete a car record from the database by ID
def delete_car(car_id):
    conn = sqlite3.connect("car_database.db")
    c = conn.cursor()
    c.execute("DELETE FROM cars WHERE id = ?", (car_id,))
    conn.commit()
    conn.close()

# Main Streamlit app
def main():
    st.title("Car Database Management")
    
    # Initialize the database
    init_db()

    # Sidebar options
    menu = ["Add Car", "View Cars", "Delete Car"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Car":
        st.subheader("Add Car Details")
        with st.form("car_form"):
            car_company = st.text_input("Car Company")
            car_model = st.text_input("Car Model")
            car_type = st.selectbox("Car Type", ["Sedan", "SUV", "Hatchback", "Convertible", "Other"])
            car_number = st.text_input("Car Number")
            plate_number = st.text_input("Plate Number")
            kilometers_driven = st.number_input("Kilometers Driven", min_value=0, step=1)
            mileage = st.number_input("Mileage (km/l)", min_value=0.0, step=0.1)
            
            submit_button = st.form_submit_button("Add Car")
        
        if submit_button:
            if car_company and car_model and car_number and plate_number:
                add_car(car_company, car_model, car_type, car_number, plate_number, kilometers_driven, mileage)
                st.success("Car data added successfully!")
            else:
                st.error("Please fill in all required fields.")

    elif choice == "View Cars":
        st.subheader("View All Cars")
        cars = get_all_cars()
        if cars:
            for car in cars:
                st.write(f"**Car ID:** {car[0]}")
                st.write(f"**Company:** {car[1]}")
                st.write(f"**Model:** {car[2]}")
                st.write(f"**Type:** {car[3]}")
                st.write(f"**Car Number:** {car[4]}")
                st.write(f"**Plate Number:** {car[5]}")
                st.write(f"**Kilometers Driven:** {car[6]}")
                st.write(f"**Mileage:** {car[7]} km/l")
                st.markdown("---")
        else:
            st.warning("No cars found in the database.")

    elif choice == "Delete Car":
        st.subheader("Delete Car")
        cars = get_all_cars()
        if cars:
            car_ids = [car[0] for car in cars]
            car_id_to_delete = st.selectbox("Select Car ID to Delete", car_ids)
            
            if st.button("Delete"):
                delete_car(car_id_to_delete)
                st.success(f"Car with ID {car_id_to_delete} has been deleted!")
        else:
            st.warning("No cars available to delete.")

if __name__ == "__main__":
    main()
