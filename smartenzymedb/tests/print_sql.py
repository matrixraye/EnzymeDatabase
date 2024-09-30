from flask_sqlalchemy.model import Model
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.ddl import CreateTable, CreateIndex

from smartenzymedb import models as models


def print_table_creation_sql(table):
    print(CreateTable(table).compile(dialect=postgresql.dialect()))
    for index in table.indexes:
        print(CreateIndex(index).compile(dialect=postgresql.dialect()))


if __name__ == '__main__':
    print_table_creation_sql(models.BasicInformation.__table__)
    print_table_creation_sql(models.Substrate.__table__)
    print_table_creation_sql(models.KineticParameters.__table__)
    print_table_creation_sql(models.StructureInformation.__table__)
    print_table_creation_sql(models.ReactionCalculation.__table__)
    print_table_creation_sql(models.Comment.__table__)
    print_table_creation_sql(models.User.__table__)
