from backend.database import SessionLocal
from backend.models import Post

dummy_posts = [
    {
        "category": "광주·전라권",
        "title": "양림동 감성 골목 산책 추천",
        "content": "주말 오전에 방문했는데 한적해서 사진 찍기 좋았습니다. 골목마다 분위기가 달라 천천히 걸어보는 걸 추천합니다.",
        "password": "1234",
        "image_url": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=800"
    },
    {
        "category": "광주·전라권",
        "title": "무등산 초보 등산 후기",
        "content": "등산을 자주 하지 않아도 부담 없이 다녀올 수 있었습니다. 정상까지는 힘들지만 중간 전망도 충분히 좋았습니다.",
        "password": "1234",
        "image_url": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800"
    },
    {
        "category": "광주·전라권",
        "title": "담양 메타세쿼이아길 힐링 코스",
        "content": "평일 오전에 가면 사람이 적고 사진도 예쁘게 나옵니다. 근처 죽녹원도 함께 방문하면 좋아요.",
        "password": "1234",
        "image_url": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800"
    },
    {
        "category": "광주·전라권",
        "title": "송정역 떡갈비 맛집",
        "content": "기차 타기 전에 들렀는데 음식도 빨리 나오고 맛도 괜찮았습니다. 관광객이 많으니 식사 시간은 조금 피하세요.",
        "password": "1234",
        "image_url": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800"
    },
    {
        "category": "광주·전라권",
        "title": "전주 한옥마을 야경 추천",
        "content": "낮보다 해질 무렵 분위기가 훨씬 좋았습니다. 한복 입고 사진 찍는 분들도 많았어요.",
        "password": "1234",
        "image_url": "https://images.unsplash.com/photo-1514565131-fce0801e5785?w=800"
    },
    {
        "category": "광주·전라권",
        "title": "여수 밤바다 드라이브",
        "content": "돌산대교 야경이 정말 예뻤습니다. 밤에 산책하기에도 좋고 근처 카페도 분위기가 좋았습니다.",
        "password": "1234",
        "image_url": "https://images.unsplash.com/photo-1500375592092-40eb2168fd21?w=800"
    }
]


def seed_posts():
    db = SessionLocal()

    try:
        # 이미 게시글이 있으면 종료
        count = db.query(Post).count()

        if count > 0:
            print(f"이미 {count}개의 게시글이 존재합니다.")
            print("더미 데이터를 추가하지 않습니다.")
            return

        posts = [Post(**data) for data in dummy_posts]

        db.add_all(posts)
        db.commit()

        print(f"{len(posts)}개의 더미 게시글을 추가했습니다.")

    except Exception as e:
        db.rollback()
        print("오류 발생:", e)

    finally:
        db.close()


if __name__ == "__main__":
    seed_posts()