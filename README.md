# The_Glory

전통주*커뮤니티*프로젝트
django humanize library

크롤링(최종현, 민경환) - 종료

우리가 할거
--> 
1. DB 검색한다 (완료)
2. pk를 가진 detail 페이지로 이동하듯이, 개별 페이지를 준다. (완료)
3. 그래서 개별페이지(탬)에서 forms을 일괄적으로 뿌린다. (완료)
4. 부가기능 붙인다. 

5. 부가기능 구현에서 중요한 것은 DB에 save하고 DB에서 불러오는 기능을 기본으로 해서 원하는 것을 구현
- 댓글평가 --> 수업시간에 한거 (댓글) --> related_name --> comment내용을 다시 뿌리려고 역참조 기능을 넣거지. 
- 별점매기기 --> 그래프 그리기 전, 6개 컬럼에 들어갈 DB짜고, 이를 저장하고, 역참조기능으로 다시 꺼내요는 그런 방식으로 이루어지고, 별모양을 django에서 구현해줄지는 모르겠고, 아무튼 jquery에는 있을듯? --> db끌어다가 ajax 통신으로 html에 뿌려주는 방식으로 진행하면 될듯. --> 있으면 받으면 더좋음 

- 그래프그리기 --> tal db의 id를 포린키로 가져오고, 육각도형 각 축에 들어가는 것을 input 칼럼으로 잡고, 평가의 평균값을 계산하여 그 최종 값을 육각그래프로 그린다. --> 하나의 술에 여러 평가가 있으니, 그래서 포린키를 가져오고, tal.objects.filter(pk=1)--> id=1인 애들의 평가가 숫자로 오겠지? --> 그걸 후처리해서 육각그래프 그리겠지. 
--> detail/1/ --> 평가들을 싹 긁어오고, 그걸 백에서 평균값 내서 리턴해줘서 html에서 이를 받아주는 비지니스 로직이 있어야함. 

8. 페이지 디자인 --> 이거 누가 할꺼야 
-  메인페이지 CSS 쉬운부분 - 민경환 
-  디테일페이지 술소개부분 CSS 빡센부분 - 박영광 
-  댓글 부분 CSS 중간난이도 - 최종현 
- login, register CSS - 민경환 ㅠ
