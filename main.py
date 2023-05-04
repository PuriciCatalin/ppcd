from mpi4py import MPI
import random

# Community
comm = MPI.COMM_WORLD
# Rank & Sizes
rank = comm.Get_rank()
size = comm.Get_size()


# Define helper function to construct number
def construct_number(x, y=None, z=None):
    number = str(x)
    if y is not None:
        number = str(y) + number
    if z is not None:
        number = str(z) + number
    return int(number)


if rank == 0:
    x0 = random.randint(1, 9)  # Generate x0
    print(f"Process {rank} generated x0 = {x0}")
    comm.send(x0, dest=1)  # Send x0 to process 1
    number = comm.recv(source=3)  # Receive number from process 3
    print(f"Process {rank} received number {number} from process 3")

if rank == 1:
    x0 = comm.recv(source=0)  # Receive x0 from process 0
    x1 = random.randint(1, 9)  # Generate x1
    number = construct_number(x1, x0)  # Construct number
    print(f"Process {rank} generated x1 = {x1}, constructed number {number}")
    comm.send(number, dest=2)  # Send number to process 2

if rank == 2:
    number = comm.recv(source=1)  # Receive number from process 1
    x2 = random.randint(1, 9)  # Generate x2
    number = construct_number(x2, number)  # Construct number
    print(f"Process {rank} generated x2 = {x2}, constructed number {number}")
    comm.send(number, dest=3)  # Send number to process 3

if rank == 3:
    number = comm.recv(source=2)  # Receive number from process 2
    x3 = random.randint(1, 9)  # Generate x3
    number = construct_number(x3, number)  # Construct number
    print(f"Process {rank} generated x3 = {x3}, constructed number {number}")
    comm.send(number, dest=0)  # Send number to process 0
