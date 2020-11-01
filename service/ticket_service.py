#todo
def count_reserved(show):
    return 5


def count_left(show) -> int:
    reserved = count_reserved(show)
    return show.room.capacity - reserved
