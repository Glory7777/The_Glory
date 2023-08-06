// 페이지가 로드되면 실행됩니다.
window.addEventListener('load', function() {
    // 네비게이션 바의 DOM 요소를 가져옵니다.
    const navBar = document.querySelector('.nav-bar');

    // 네비게이션 바의 초기 위치 정보를 가져옵니다.
    const navBarTop = navBar.offsetTop;

    // 스크롤 이벤트를 감지합니다.
    window.addEventListener('scroll', function() {
        // 현재 스크롤 위치를 가져옵니다.
        const currentScrollPos = window.scrollY;

        // 스크롤 위치가 네비게이션 바의 초기 위치를 넘어서면 고정합니다.
        if (currentScrollPos >= navBarTop) {
            // 네비게이션 바를 상단에 고정시킵니다.
            navBar.style.position = 'fixed';
            navBar.style.top = '0';
        } else {
            // 네비게이션 바의 고정을 해제합니다.
            navBar.style.position = 'static';
        }
    });
});