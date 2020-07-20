/**********  NAVBAR SLIDE IN FUNCTION **********/
const navSlide = () => {
    const burger = document.querySelector('.burger');
    const nav = document.querySelector('.nav-links');
    const navLinks = document.querySelectorAll('.nav-links li')

    
    burger.addEventListener('click', ()=>{
        //toggle nav
        nav.classList.toggle('nav-active');

        //fade in links
        navLinks.forEach((link, index)=>{
            if (link.style.animation){
                link.style.animation = '';
            }
            else{
                link.style.animation = `navLinkFade 0.4s ease forwards ${index/7 +0.4}s`
            }
        });

        //burger animation
        burger.classList.toggle('toggle-burger');
    });
}

/********** TAB FUNCTION **********/
const makeTabs = () => {
    const tabs = document.querySelectorAll('[data-tab-target]');
    const tabContents = document.querySelectorAll('[data-tab-content]');

    tabs.forEach(tab =>{
        tab.addEventListener('click', () => {
            tabContents.forEach(tabContent => {
                tabContent.classList.remove('active'); // on click remove active class from all elements of type [data-tab-content] 
            });
            tabs.forEach(tab => {
                tab.classList.remove('active'); // on click remove active class from all elements of type [data-tab-content] 
            });
            const target = document.querySelector(tab.dataset.tabTarget);
            target.classList.add('active'); // on click add active class to specified [data-tab-target]
            tab.classList.add('active');
        });
    });
}

/********** ACCORDION FUNCTION **********/
const accordionSlide = () =>{
    const accordionItemHeader = document.querySelectorAll(".accordion-item-header");
    accordionItemHeader.forEach(header=>{
        header.addEventListener("click", e=>{
            header.classList.toggle("active")
            const accordionItemBody = header.nextElementSibling;
            if(header.classList.contains("active")){
                accordionItemBody.style.maxHeight = accordionItemBody.scrollHeight +"px"
            }
            else{
                accordionItemBody.style.maxHeight = 0;
            }
        })
    })
}

navSlide();
makeTabs();
accordionSlide();