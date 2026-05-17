from src.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text('SELECT 1'))
    print('Conexao com Supabase OK:', result.fetchone())