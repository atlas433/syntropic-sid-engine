from domain.entities.plant import Plant
from domain.entities.row import Row
from domain.entities.enums import RowType


class InMemoryRowRepository:
    def __init__(self):
        self._rows: dict[str, Row] = {}

    def find_all(self) -> list[Row]:
        return list(self._rows.values())

    def find_by_type(self, row_type: RowType) -> list[Row]:
        return [r for r in self._rows.values() if r.row_type == row_type]

    def save(self, row: Row) -> None:
        self._rows[row.id] = row

    def find_by_id(self, row_id: str) -> Row | None:
        return self._rows.get(row_id)


class InMemoryPlantRepository:
    def __init__(self):
        self._plants: dict[str, Plant] = {}

    def find_by_row(self, row_id: str) -> list[Plant]:
        return [p for p in self._plants.values()]

    def save(self, plant: Plant) -> None:
        self._plants[str(plant.id)] = plant
