const menu_icon = document.querySelector("#menu-icon");
const menus = document.querySelector("#mobile-menus");

menu_icon.addEventListener("click", ()=>{
    if(menus.style.display == 'flex'){
        menus.style.display = "none";
    }else {
        menus.style.display = "flex";
    }
})