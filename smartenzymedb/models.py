from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from sqlalchemy import create_engine, Column, Integer, BigInteger, String, Text, SmallInteger, DECIMAL, ForeignKey, Index
from sqlalchemy.orm import relationship

db = SQLAlchemy()   


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    ROLE_USER = 0
    ROLE_ADMIN = 30

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    _password = db.Column('password', db.String(256), nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_USER)

    __table_args__ = (
        Index('user_email_and_password_btree',
              "email", "password",
              postgresql_using='btree'
              ),
    )

    def __repr__(self):
        return '<User:{}>'.format(self.username)

    @property
    def password(self):
        """ Python 风格的 getter """
        return self._password

    @password.setter
    def password(self, orig_password):
        """ Python 风格的 setter, 这样设置 user.password 就会
        自动为 password 生成哈希值存入 _password 字段
        """
        self._password = generate_password_hash(orig_password)

    def check_password(self, password):
        """ 判断用户输入的密码和存储的 hash 密码是否相等
        """
        return check_password_hash(self._password, password)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    def get_id(self):
        return str(self.user_id)

class BasicInformation(db.Model):
    __tablename__ = 'basic_information'
    protein_id = Column(BigInteger, primary_key=True, autoincrement=True)
    ECNumber = Column(Text, nullable=False)
    ProteinName = Column(Text, nullable=False)
    Organism = Column(Text)
    UniprotID = Column(Text)
    Sequence = Column(Text)
    SequenceLength = Column(SmallInteger)
    PDBID_WT = Column(Text)
    PDBID_MUT = Column(Text)
    AlphaFoldDB = Column(Text)
    Mutation = Column(Text)
    MutatedChain = Column(Text)
    MutationCount = Column(SmallInteger)

    # Referer.
    substrate = relationship('Substrate', backref="BasicInformation", uselist=False, lazy=True)
    kinetic_parameters = relationship('KineticParameters', backref="BasicInformation", uselist=False, lazy=True)
    structure_information = relationship('StructureInformation', backref="BasicInformation", uselist=False, lazy=True)
    reaction_calculation = relationship('ReactionCalculation', backref="BasicInformation", uselist=False, lazy=True)
    comment = relationship('Comment', backref="BasicInformation", uselist=False, lazy=True)

    __table_args__ = (
        Index('basic_information_basic_cols_gin', 
              "ECNumber", "ProteinName", "UniprotID", "PDBID_WT", "PDBID_MUT", "Mutation", 
              postgresql_using='gin', 
              postgresql_ops={
                  'ECNumber': 'gin_bigm_ops', 
                  'ProteinName': 'gin_bigm_ops', 
                  'UniprotID': 'gin_bigm_ops',
                  'PDBID_WT': 'gin_bigm_ops',
                  'PDBID_MUT': 'gin_bigm_ops',
                  'Mutation': 'gin_bigm_ops'
              }
        ),
        Index('basic_information_sequence_length_btree', SequenceLength),
    )

class Substrate(db.Model):
    __tablename__ = 'substrate'
    protein_id = Column(BigInteger, ForeignKey('basic_information.protein_id'), primary_key=True)
    Substrate = Column(Text)
    Smiles = Column(Text)
    MolecularFormula = Column(Text)
    Cofator = Column(Text)
    ProductFormula = Column(Text)

    __table_args__ = (
        Index('substrate_basic_cols_gin', 
              "Substrate", 
              postgresql_using='gin', 
              postgresql_ops={
                  'Substrate': 'gin_bigm_ops'
              }
        ),
    )

class KineticParameters(db.Model):
    __tablename__ = 'kinetic_parameters'
    protein_id = Column(BigInteger, ForeignKey('basic_information.protein_id'), primary_key=True)
    Activity = Column(DECIMAL(11, 5))
    KM = Column(DECIMAL(11, 5))
    Kcat = Column(DECIMAL(11, 5))
    KMPerKcat = Column(DECIMAL(11, 5))
    TN = Column(DECIMAL(11, 5))
    EValue = Column(DECIMAL(11, 5))
    DeltaDeltaG = Column(DECIMAL(11, 5))
    Temperature = Column(SmallInteger)
    pH = Column(DECIMAL(7, 5))

    # Indices
    __table_args__ = (
        Index('kinetic_parameters_activity_btree', Activity, postgresql_using='btree'),
        Index('kinetic_parameters_km_btree', KM, postgresql_using='btree'),
        Index('kinetic_parameters_kcat_btree', Kcat, postgresql_using='btree'),
        Index('kinetic_parameters_kmperkcat_btree', KMPerKcat, postgresql_using='btree'),
        Index('kinetic_parameters_tn_btree', TN, postgresql_using='btree'),
        Index('kinetic_parameters_evalue_btree', EValue, postgresql_using='btree'),
        Index('kinetic_parameters_deltadeltag_btree', DeltaDeltaG, postgresql_using='btree'),
        Index('kinetic_parameters_temperature_btree', Temperature, postgresql_using='btree'),
        Index('kinetic_parameters_ph_btree', pH, postgresql_using='btree'),
    )

class StructureInformation(db.Model):
    __tablename__ = 'structure_information'
    protein_id = Column(BigInteger, ForeignKey('basic_information.protein_id'), primary_key=True)
    RSA = Column(DECIMAL(11, 5))
    PHI = Column(DECIMAL(11, 5))
    PSI = Column(DECIMAL(11, 5))
    ResidueDepth = Column(DECIMAL(11, 5))
    CADepth = Column(DECIMAL(11, 5))
    RelativeBfactor = Column(DECIMAL(11, 5))

class ReactionCalculation(db.Model):
    __tablename__ = 'reaction_calculation'
    protein_id = Column(BigInteger, ForeignKey('basic_information.protein_id'), primary_key=True)
    ActiveResidue = Column(Text)
    ReactionSmile = Column(Text)
    KEGG = Column(Text)
    ReactionEnergy = Column(DECIMAL(11, 5))
    ReactionParameters = Column(Text)

class Comment(db.Model):
    __tablename__ = 'comment'
    protein_id = Column(BigInteger, ForeignKey('basic_information.protein_id'), primary_key=True)
    Literature = Column(Text)
    DOI = Column(Text)
    Year = Column(SmallInteger)
    PMID = Column(Text)

    # Index
    __table_args__ = (
        Index('comment_year_btree', Year),
        Index('comment_basic_cols_gin', PMID, postgresql_using='gin'),
    )