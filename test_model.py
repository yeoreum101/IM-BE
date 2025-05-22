import sqlite3
import os
import traceback
import json
from datetime import datetime

try:
    # 데이터베이스 파일 경로 설정 - 올바른 경로 구분자 사용
    db_path = os.path.join("C:\\Users", "khmin", "OneDrive", "문서", "GitHub", "IM-BE", "instance", "app.db")
    print(f"데이터베이스 파일 경로: {db_path}")
    
    # 경로가 존재하는지 확인
    db_dir = os.path.dirname(db_path)
    if not os.path.exists(db_dir):
        print(f"디렉토리가 존재하지 않습니다: {db_dir}")
        os.makedirs(db_dir, exist_ok=True)
        print(f"디렉토리를 생성했습니다: {db_dir}")
    else:
        print(f"디렉토리가 이미 존재합니다: {db_dir}")
    
    # SQLite 데이터베이스 직접 연결
    print(f"SQLite 데이터베이스 연결 시도: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 테이블 생성
    print("테이블 생성 시도...")
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS member_tb (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        google_id TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS music_tb (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        music_url TEXT NOT NULL,
        title TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 기존 데이터 확인
    cursor.execute("SELECT COUNT(*) FROM member_tb")
    member_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM music_tb")
    music_count = cursor.fetchone()[0]
    
    print(f"기존 데이터 수: Member={member_count}, Music={music_count}")
    
    # 데이터 삽입 (이미 있는 경우 다른 ID로 시도)
    try:
        print("Member 데이터 삽입 시도...")
        cursor.execute(
            'INSERT INTO member_tb (google_id, name) VALUES (?, ?)',
            (f'test_google_id_{member_count}', 'Test User')
        )
        print("Member 데이터 삽입 완료")
    except sqlite3.IntegrityError:
        print("Member 삽입 중 중복 오류 발생, 다른 ID로 시도합니다")
        cursor.execute(
            'INSERT INTO member_tb (google_id, name) VALUES (?, ?)',
            (f'test_google_id_{datetime.now().timestamp()}', 'Test User')
        )
    
    try:
        print("Music 데이터 삽입 시도...")
        cursor.execute(
            'INSERT INTO music_tb (music_url, title) VALUES (?, ?)',
            (f'https://example.com/test{music_count}.mp3', 'Test Music')
        )
        print("Music 데이터 삽입 완료")
    except sqlite3.IntegrityError:
        print("Music 삽입 중 중복 오류 발생, 다른 URL로 시도합니다")
        cursor.execute(
            'INSERT INTO music_tb (music_url, title) VALUES (?, ?)',
            (f'https://example.com/test_{datetime.now().timestamp()}.mp3', 'Test Music')
        )
    
    conn.commit()
    
    # 데이터 조회
    print("\nMember 조회...")
    cursor.execute('SELECT * FROM member_tb LIMIT 5')
    members = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    
    for member in members:
        member_dict = dict(zip(columns, member))
        print(f"Member: {json.dumps(member_dict, default=str)}")
    
    print("\nMusic 조회...")
    cursor.execute('SELECT * FROM music_tb LIMIT 5')
    musics = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    
    for music in musics:
        music_dict = dict(zip(columns, music))
        print(f"Music: {json.dumps(music_dict, default=str)}")
    
    # 연결 종료
    conn.close()
    print("\nSQLite 데이터베이스 테스트 성공!")
    print(f"데이터베이스 파일: {db_path}")
except Exception as e:
    print(f"오류 발생: {str(e)}")
    traceback.print_exc()