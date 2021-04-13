import sys
import re


def automated_ticketing_system(input_file):
    """
    :param input_file: File contain a set of commands separated by a newline.
    Execute the commands in order and produce output.
    """
    with open(input_file, "r") as f:
        """ set of unprocessed commands e.g. - Create_parking_lot 6\n"""
        unprocessed_input_commands = f.readlines()
        print(unprocessed_input_commands)
    """ set of processed commands e.g. - Create_parking_lot 6"""
    input_commands = [command.replace("\n", "") for command in unprocessed_input_commands]

    try:
        """Executing first command"""
        command = input_commands.pop(0)
        maximum_number_of_parking_slots = int(re.findall('Create_parking_lot (\d+)', command)[0])
        print('Created parking of {} slots'.format(maximum_number_of_parking_slots))
    except Exception as e:
        print('Please provide the valid command to create the parking lot e.g. - "Create_parking_lot 6"')
        return

    parking_slots = {}
    while input_commands:
        """Executing command"""
        command = input_commands.pop(0)

        if 'Park' in command and 'driver_age' in command:
            """
            When a car enters the parking lot, we want to have a ticket issued to the driver
            """
            if len(parking_slots.keys()) >= maximum_number_of_parking_slots:
                print('All parking slots are full')
                continue
            else:
                """Customer should be allocated a parking slot that is nearest to the entry"""
                nearest_parking_slot_available = min(set(range(1, maximum_number_of_parking_slots+1)
                                                         ) - set([int(i) for i in parking_slots.keys()]))
            vehicle_number = command.split(' ')[1]
            """
            Taking note of the number written on the vehicle registration plate and age of the driver.
            Allocation an available parking slot to the car before actually handing over a tickets to the driver.
            """
            parking_slots['{}'.format(nearest_parking_slot_available)] = {
                'parking_slot_number': nearest_parking_slot_available,
                'vehicle_number': command.split(' ')[1],
                'age': int(command.split(' ')[3])}
            print('Car with vehicle registration number "{}" has been parked at slot number {}'.format(
                vehicle_number, nearest_parking_slot_available))

        elif 'Slot_numbers_for_driver_of_age' in command:
            """
            Slot numbers of all slots where cars of drivers of a particular age are parked.
            """
            age = int(command.split(' ')[1])
            slot_numbers = [str(parking_slot['parking_slot_number']) for parking_slot in parking_slots.values()
                            if parking_slot['age'] == age]
            if slot_numbers:
                print(','.join(slot_numbers))
            else:
                print('No parked car matches the query')

        elif 'Slot_number_for_car_with_number' in command:
            """
            Slot number in which a car with a given vehicle registration plate is parked
            """
            vehicle_number = command.split(' ')[1]
            slot_numbers = [str(parking_slot['parking_slot_number']) for parking_slot in parking_slots.values()
                            if parking_slot['vehicle_number'] == vehicle_number]
            if slot_numbers:
                print(','.join(slot_numbers))
            else:
                print('No parked car matches the query')

        elif 'Vehicle_registration_number_for_driver_of_age' in command:
            """
            vehicle registration numbers for all cars which are parked by the driver of certain age
            """
            requested_age = int(command.split(' ')[1])
            vehicle_numbers = [str(parking_slot['vehicle_number']) for parking_slot in parking_slots.values()
                               if parking_slot['age'] == requested_age]
            if vehicle_numbers:
                print(','.join(vehicle_numbers))
            else:
                print('No parked car matches the query')

        elif 'Leave' in command:
            """
            At the exit, the customer returns the ticket which then marks the slot they were using as being available
            """
            slot_number = int(command.split(' ')[1])
            try:
                vacated_parking_slot = parking_slots.pop('{}'.format(slot_number))
                print('Slot number {} vacated, the car with vehicle registration number "{}" '
                      ' left the space, the driver of the car was of age {}'.format(
                        vacated_parking_slot['parking_slot_number'],
                        vacated_parking_slot['vehicle_number'],
                        vacated_parking_slot['age'],
                        ))
            except KeyError:
                print("Slot already vacant")


if __name__ == "__main__":

    try:
        file = sys.argv[1]
        automated_ticketing_system(input_file=file)
    except IndexError:
        print('Please provide the valid file e.g. - input.txt')
