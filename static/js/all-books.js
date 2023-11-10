
var currentSelectedCategory = '';
var maturityRating = 'All';
var currentBooks = [];
var currentfilterBooks= [];
var categoryMap = new Map();
var currentSearchCategory = 'All';
var isBooksDropdownOpen = false;
var isBooksDropdownMobileOpen = false;
let startX = 0;
let endX = 0;
const NO_THUMBNAIL_URL = 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/495px-No-Image-Placeholder.svg.png?20200912122019'
const bookDropdownButton = document.querySelectorAll(".dropdown-button-xl");
//document.getElementsByClassName()
const bookDropdownContent = document.querySelectorAll(".books-dropdown-content");
const bookDropdownValues = document.querySelectorAll(".books-dropdown-values");
const currentBooksDropdownValuesElement = document.querySelectorAll(".books-dropdown-current-value");
const categoriesContainer = document.getElementById('categories-container');
const bookDropdownSVG = document.querySelectorAll('.books-dropdown-svg');
let firstTime = true;

const pcSearchInput = document.getElementById('pc-search-input');
const pcSearchAnswerBtn = document.getElementById('pc-search-answer');
const mobileSearchInput = document.getElementById('mobile-search-input');
const mobileSearchAnswerBtn = document.getElementById('mobile-search-answer');

let searchText = '';

mobileSearchInput.addEventListener('input', (event) => {
    searchText = event.target.value;
    pcSearchInput.value = searchText;
 });
pcSearchInput.addEventListener('input', (event) => {
    searchText = event.target.value;
    mobileSearchInput.value = searchText;
 });

const validateSearch = () => {
    if(searchText.trim() == ''){
        return Toastify({
            text: "Maaf teks pencarian masih kosong",
            duration: 3000, // Durasi tampilan toast (dalam milidetik)
            style: {
              background: 'red', // Warna latar belakang untuk pesan sukses
              color: 'white', // Warna teks untuk pesan sukses
            },
            close:true
          }).showToast();
    }
    const searchUrl = `/search-books/${currentSearchCategory}/${searchText}`;
    window.location.href = searchUrl;

}

pcSearchAnswerBtn.addEventListener('click', ()=> {
    validateSearch()
})
mobileSearchAnswerBtn.addEventListener('click', ()=> {
    validateSearch()
})

bookDropdownButton.forEach((btn)=>{
    btn.addEventListener('click', ()=>{
        console.log('INFOKAN')
        console.log(bookDropdownSVG)
        toggleBooksDropdown()
      })
})

let mode = () => window.innerWidth < 768 ? 'MOBILE' : window.innerWidth < 1024? 'MEDIUM' : 'LARGE';


var currentPreferences = {
    sortBy: 'TERBARU',
    minYear: '',
    maxYear: '',
    maturity: 'ALL',
    saleability: 'ALL',
    star: 'default',
    minPrice: '',
    maxPrice: '',
    availability: 'default',
  };
const preferenceButton = document.getElementById('preference-btn')
const nextCategoriesButton = document.getElementById('next-categories-button');
const prevCategoriesButton = document.getElementById('prev-categories-button');
const loadingSpinner = document.getElementById('loading-text');
const homeContent = document.getElementById('homeContent');
const booksCardContainer = document.getElementById('books-card-container');
const booksCardContainerHeader = document.getElementById('books-card-container-header');
const categoriesOverlay = document.getElementById('categories-overlay');
const topDivider = document.getElementById('top-divider');
const bottomDivider = document.getElementById('bottom-divider');
const sidebarBackground = document.getElementById('sidebar-background')
let lastScrollPosition = window.scrollY;
const applyPreferenceBtn = document.getElementById('apply-preference')
let isScrolling;
const scrollThreshold = 100;
let prevWidth = window.innerWidth;
const booksSidebar = document.getElementById('books-sidebar');
var isBooksSidebarOpen = false;
const booksDropdownKey = []

const setMode = () => {
    if(mode() == 'MOBILE'){
        bookDropdownContent[0].className = `max-h-[24rem] hidden absolute top-12 right-0 z-20  bg-violet-700 divide-y divide-gray-100 rounded-lg shadow w-44 `;
        bookDropdownSVG[0].classList.remove('rotate-180');
        isBooksDropdownOpen = false;
    }
    else{
        bookDropdownContent[1].className = `max-h-[24rem] hidden absolute top-12 right-0 z-20  bg-violet-700 divide-y divide-gray-100 rounded-lg shadow w-44 `;
        bookDropdownSVG[1].classList.remove('rotate-180');
        isBooksDropdownMobileOpen = false;
    }

}
window.addEventListener('resize', setMode )

window.addEventListener('click', (event)=> {
    if(mode()== 'MOBILE'){
        if(! bookDropdownButton[1].contains(event.target)){
            return closeBooksDropdown();
        }
    }
    else{
        if(! bookDropdownButton[0].contains(event.target)){
            return closeBooksDropdown();
        }
    }
})
setMode()
const openBooksDropdown = () => {
    console.log('OKEE')
    if(mode() == 'MOBILE'){
        bookDropdownContent[1].className = `max-h-[24rem] absolute top-14 left-0 z-20  bg-violet-700 divide-y divide-gray-100 rounded-lg shadow w-44 `
        isBooksDropdownMobileOpen = true;

    }
    else{
        bookDropdownContent[0].className = `max-h-[24rem] absolute top-14 right-0 z-20  bg-violet-700 divide-y divide-gray-100 rounded-lg shadow w-44`
        isBooksDropdownOpen = true;
    }
    bookDropdownSVG.forEach(svg => {
        if(! svg.classList.contains('rotate-180')){
            svg.classList.add('rotate-180')
           }
    });
}
const closeBooksDropdown = () => {
    if(mode() == 'MOBILE'){
        bookDropdownContent[1].className = `max-h-[24rem] hidden absolute top-12 right-0 z-20  bg-violet-700 divide-y divide-gray-100 rounded-lg shadow w-44 `
        isBooksDropdownMobileOpen = false;
    }
    else{
        bookDropdownContent[0].className = `max-h-[24rem] hidden absolute top-12 right-0 z-20  bg-violet-700 divide-y divide-gray-100 rounded-lg shadow w-44`
        isBooksDropdownOpen = false;
    }
    bookDropdownSVG.forEach(svg => {
        svg.classList.remove('rotate-180');
    });
}
const setSidebarStateResize = () => {
    const currentWidth = window.innerWidth;
    const isMedium = (width) => width >= 768 && width < 1024;
    const isLarge = (width) => width >= 1024;
    const isSmall = (width) => width < 768;

    if((isMedium(currentWidth) || isSmall(currentWidth)) && isLarge(prevWidth)){
        if(!isBooksSidebarOpen){
            hideBookSidebar()
        }
    }

    if(isLarge(currentWidth) && isBooksSidebarOpen){
        hideBookSidebar()
    }

    if(isLarge(currentWidth)){
        booksSidebar.style.transform = 'translateX(0)'
        sidebarBackground.style.display = 'none'
    }

    prevWidth = currentWidth;
}

preferenceButton.addEventListener('click', ()=> {
    openBookSidebar()
})
window.addEventListener('resize', ()=> {
    setSidebarStateResize()
})
setSidebarStateResize()

const hideBookSidebar = () => {
    sidebarBackground.style.display = 'none';
    booksSidebar.style.transform = 'translateX(28rem)';
    isBooksSidebarOpen = false;
}
sidebarBackground.addEventListener('click', ()=>{
    hideBookSidebar()
})
const openBookSidebar = () => {
    sidebarBackground.style.display = 'flex'
    booksSidebar.style.transform = 'translateX(0)'
    isBooksSidebarOpen = true;

}


const  userPublishTime = (timestamp) => {
    // Konversi timestamp ke objek Date
    const eventTime = new Date(timestamp);
  
    // Waktu saat ini
    const currentTime = new Date();
  
    // Hitung selisih waktu dalam milidetik
    const timeDifference = currentTime - eventTime;
  
    // Hitung selisih waktu dalam detik, menit, jam, dan hari
    const seconds = Math.floor(timeDifference / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);
  
    if (days >= 1) {
      return `${days} hari yang lalu`;
    } else if (hours >= 1) {
      return `${hours} jam yang lalu`;
    } else if (minutes >= 1) {
      return `${minutes} menit yang lalu`;
    } else {
      return 'Baru saja';
    }
  }
  

const sortCategory = (books) => {
    categoryMap = new Map()
    categoryMap.set('All', 0)
    books.forEach(book => {
        if(categoryMap.has('All')){
            categoryMap.set('All', categoryMap.get('All') + 1)
        }
        book.categories.forEach(category => {
            if(categoryMap.has(category)){
                categoryMap.set(category, categoryMap.get(category) + 1);
            }
            else{
                categoryMap.set(category, 1);
            }
        })
    })
    categoryMap =  new Map([...categoryMap.entries()].sort((a, b) => b[1] - a[1]));
}

const setBooksPreference = () => {
    let books = currentBooks;
    const sortBy = currentPreferences.sortBy;
    const filterByMaturityRating = currentPreferences.maturity == 'ALL'? (maturityRating) => true :
    currentPreferences.maturity == 'NOT_MATURE'? (maturityRating) => maturityRating.toUpperCase() == 'NOT_MATURE' :
    (maturityRating) => maturityRating.toUpperCase() == 'MATURE';
    const filterByYearRange = (min,max,year) => !year? true :  currentPreferences.minYear == '' && currentPreferences.maxYear == ''?
    (min,max,year)=> true : currentPreferences.minYear == ''? (min,max,year)=> year <= parseFloat(max) :
    currentPreferences.maxYear == ''? (min,max,year)=> year >= parseFloat(min) : (min,max,year) =>
    year <= max && year >= min;
    const filterBySalebiality = currentPreferences.saleability == 'ALL'? (saleability) => true :
    currentPreferences.saleability == 'FREE'? (saleability) => saleability == false:
    (saleability) => saleability == true;
    //todo: star rating
    const filterByStarRating = (star)=> true;
    const filterByPrice = currentPreferences.maxPrice == '' && currentPreferences.minPrice == ''?
    (min, max, price)=> true : currentPreferences.maxPrice == ''? (min, max, price) => price >= parseFloat(min) :
    currentPreferences.minPrice == ''? (min, max, price )=> price <= parseFloat(max) :
    (min,max,price) => price <= parseFloat(max) && price >= parseFloat(min);
    const filterByAvailability = currentPreferences.availability == 'default'? (pdf,epub) => true :
    currentPreferences.availability == 'PDF'? (pdf,epub) => pdf == true :
    (pdf,epub) => epub == true;
    books.sort((firstBook, secondBook)=> {
        if(sortBy == 'TERBARU'){
            return new Date(secondBook.user_publish_time) - new Date(firstBook.user_publish_time)
        }
        if(sortBy == 'TERLAMA'){
            return new Date(firstBook.user_publish_time) - new Date(secondBook.user_publish_time)
        }
        if(sortBy == 'PALING_BANYAK_DISUKAI'){
            return 0;
        }
        if(sortBy == 'REVIEW_TERBANYAK'){
            return 0;
        }
    });
    if(currentSelectedCategory != 'All'){
        books = books.filter((book)=>{
            if(!book.categories){
                return false;
            }
            if(book.categories.includes(currentSelectedCategory)){
                return true;
            }
            return false;
        })
    };
    books = books.filter((book)=> {
        if(currentPreferences.saleability == 'FREE'){
            return filterByMaturityRating(book.maturity_rating) && 
            filterByYearRange(currentPreferences.minYear, currentPreferences.maxYear,
             parseFloat(book.published_date.split("-")[0])) &&
            filterBySalebiality(book.saleability) &&
            filterByAvailability(book.pdf_available, book.epub_available)
        }
        return filterByMaturityRating(book.maturity_rating) && 
            filterByYearRange(currentPreferences.minYear, currentPreferences.maxYear,
            book.published_date? parseFloat(book.published_date.split("-")[0]) : null) &&
            filterBySalebiality(book.saleability) &&
            filterByAvailability(book.pdf_available, book.epub_available) &&
            filterByPrice(currentPreferences.minPrice, currentPreferences.maxPrice, parseFloat(book.price?? '0'))

    })
    currentfilterBooks = [...books];
    console.log('ini buku yang anda minta-> ', books);
    wrapperSetBooks(currentfilterBooks);
    if(mode() != 'LARGE'){
        hideBookSidebar()
    }
    
}

applyPreferenceBtn.addEventListener('click', ()=> {
    let preferences = getPreferences();
    if(preferences){
        currentPreferences = preferences
        console.log('MINIMAL DISINI AMAN')
        setSelectedCategory(currentSelectedCategory)
    }
})

window.addEventListener('scroll', () => {
    const currentScrollPosition = window.scrollY;
    clearTimeout(isScrolling);
    isScrolling = setTimeout(()=> {
        categoriesOverlay.style.transform = 'translateY(0)';
    }, scrollThreshold)
    if (currentScrollPosition > lastScrollPosition) {
      // Scrolling down
      
      categoriesOverlay.style.transform = 'translateY(-400%)';
    } else {
      // Scrolling up
      categoriesOverlay.style.transform = 'translateY(0)';
      
    }
  
    lastScrollPosition = currentScrollPosition;
    
  });

const getPreferences = () => {
    let preferences = {};
    let error = false
  
    // Mendapatkan nilai "Sort By"
    preferences.sortBy = document.querySelector('input[name="sortBy"]:checked').value;
  
    // Mendapatkan nilai "Year Range"
    preferences.minYear = document.getElementById('minYear').value;
    preferences.maxYear = document.getElementById('maxYear').value;
  
    // Mendapatkan nilai "Maturity Rating"
    preferences.maturity = document.querySelector('input[name="maturity"]:checked').value;
  
    // Mendapatkan nilai "Saleability Option"
    preferences.saleability = document.querySelector('input[name="saleability"]:checked').value;
  
    // Mendapatkan nilai "Average Ratings"
    preferences.star = document.querySelector('input[name="star"]:checked').value;
  
    // Mendapatkan nilai "Price Range"
    preferences.minPrice = document.getElementById('minPrice').value;
    preferences.maxPrice = document.getElementById('maxPrice').value;
    
    // Mendapatkan nilai "Availability"
    preferences.availability = document.querySelector('input[name="availability"]:checked').value;

    //if(preferences.minPrice )

    if(preferences.minPrice != "" && preferences.maxPrice != ""){
        if(parseFloat(preferences.minPrice) > parseFloat(preferences.maxPrice)){
            showError('Harga minimal tidak boleh melebihi harga maksimal');
            error = true;
        }
    }

    if(preferences.minPrice != ""){
        if(parseFloat(preferences.minPrice) < 0){
            showError('Harga tidak boleh negatif');
            error = true;
        }
    }
    if(preferences.maxPrice != ""){
        if(parseFloat(preferences.maxPrice) < 0){
            showError('Harga tidak boleh negatif');
            error = true;
        }
    }

    if(preferences.minYear != ""){
        if(parseFloat(preferences.minYear) < 1978){
            showError('Tahun minimal adalah 1978');
            error = true;
        }
        if(parseFloat(preferences.minYear) > 2023){
            showError('Tahun maksimal adalah 2023');
            error = true;
        }
    }
    if(preferences.maxYear != ""){
        if(parseFloat(preferences.maxYear) < 1978){
            showError('Tahun minimal adalah 1978');
            error = true;
        }
        if(parseFloat(preferences.maxYear) > 2023){
            showError('Tahun maksimal adalah 2023');
            error = true;
        }
    }

    if(preferences.minYear != "" && preferences.maxYear != ""){
        if(parseFloat(preferences.minYear) > parseFloat(preferences.maxYear)){
            showError('Tahun minimal tidak boleh melebihi tahun maksimal');
            error = true;
        }
        
    }
    if(error){
        document.getElementById('minPrice').value = "";
        document.getElementById('maxPrice').value = "";
        document.getElementById('minYear').value = "";
        document.getElementById('maxYear').value = "";
        return null;
    }
  
    return preferences;
  }

const showSuccess = (message) => {
    return Toastify({
        text: message,
        duration: 3000, // Durasi tampilan toast (dalam milidetik)
        style: {
          background: 'green', // Warna latar belakang untuk pesan sukses
          color: 'white', // Warna teks untuk pesan sukses
        },
        close:true
      }).showToast();
}

const showError = (message) => {
    return Toastify({
        text: message,
        duration: 3000, // Durasi tampilan toast (dalam milidetik)
        style: {
          background: 'red', // Warna latar belakang untuk pesan sukses
          color: 'white', // Warna teks untuk pesan sukses
        },
        close:true
      }).showToast();
}
const wrapperSetBooks = (res) => {
    loadingSpinner.style.display = 'flex';
    setTimeout(()=> {
        setBooks(res);
        loadingSpinner.style.display = 'none';
    }, 1200)
}

const getBooks = async ()=>{
    try {
        const resJson = await fetch('/get-books/', {
            method:'GET'
        });
        const res = await resJson.json();
        console.log(res);
        const books = res.books;
        books.reverse();
        currentBooks = [...books];
        setBooks(currentBooks)

    } catch (error) {
        console.log(error)
    }
}

const setBooks = (res) => {
    let booksString = '';
    try {
        if(res.length == 0){
            booksCardContainer.className = "flex flex-col items-center justify-center px-1 w-full pb-24 grow";
    
            topDivider.style.display = 'none';
            bottomDivider.style.display = 'none';
            booksCardContainer.innerHTML = `
            <div class=' min-w-[12rem] w-[15%] h-auto'>
                <img class='w-full h-full' src="/static/img/empty.svg" >
            </div>
            <div class="text-lg font-bold flex w-full justify-center mt-3">
            Maaf Buku Tidak Ada.
            </div>
            `
            return;
        }
        booksCardContainer.className = "grid  md:grid-cols-2 lg:grid-cols-3  gap-y-2 w-full px-1 grid-flow-row auto-rows-max";
        topDivider.style.display = 'flex';
        bottomDivider.style.display = 'flex';
        res.forEach((book,index) => {
            const isFirstLast = index == res.length -1;
            const isSecondLast = index == res.length -2;
            const isThirdLast = index == res.length -3;
            const bookString = `
            <div  class="flex-auto flex flex-col  ">
                    <div class="  w-full px-2 grow flex  min-h-[13rem]  py-2">
                        <img class="rounded-md h-[10rem] aspect-[3/4]" src=${book.thumbnail? book.thumbnail : NO_THUMBNAIL_URL } alt="">
                        <div class=" pl-3 flex-1 flex flex-col min-h-full ">
                            <div class="flex  justify-between items-start ">
                            <div class="mt-1 mr-2">
                            
                            <a class="font-bold text-sm line-clamp-2 text-[#460C90]" href="/detail/book-detail/${book.id}">${ book.title ? book.title : 'No Title' }</a>
                            
                            <h1 class="text-gray-400 text-xs line-clamp-2">
                            ${book.authors.length > 0 ? book.authors.map((author,index)=>{
                                if(index == book.authors.length - 1){
                                    return `<a>${author}</a><span>.</span>`
                                }
                                return `<a>${author}</a><span>, </span>`
                            }) : 'Unknown'}
                            </h1>
                        </div>  
                                
                                <div class="ml-auto flex flex-col items-center justify-center">
                                    <div class=" fas fa-heart text-red-500 text-lg">
                                    </div>
                                    <h1 class="text-xs">1024</h1>
                                </div>
                            </div>
                            
                            <div class="text-xs text-gray-400 mt-1">
                                Created by <span class="text-[#460C90]">Isa Citra</span>
                            </div>
                            <div class="mt-1 flex items-center space-x-2">
                                <div class="rating text-yellow-400 text-sm">
                                    <span class="fas fa-star"></span>
                                    <span class="fas fa-star"></span>
                                    <span class="fas fa-star"></span>
                                    <span class="fas fa-star"></span>
                                    <span class="fas fa-star-half-alt"></span>
                                </div> 
                                <div class="text-xs text-gray-400">
                                    415 Reviews
                                </div>
                            </div>    
                            <div  class="mt-1 text-gray-400 text-xs line-clamp-2">
                                ${book.categories.length > 0 ? book.categories.map((category,index)=>{
                                    if(index == book.categories.length - 1){
                                        return `<a>${category}</a><span>.</span>`
                                    }
                                    return `<a>${category}</a><span>, </span>`
                                }) : 'No categories'}
                            </div>
                            <div  class="mt-2 text-[#C52A62] font-bold text-sm line-clamp-2">
                                ${book.currencyCode && book.price? `${book.currencyCode} <span>${book.price}</span>` : 'FREE'}
                            </div>
                            <div class="mt-auto ml-auto text-xs text-gray-500">
                                ${userPublishTime(book.user_publish_time)}
                            </div>
                        </div>
                    </div>
                    <div class="mt-auto border-b border-[#460C90] w-full opacity-20 ${isFirstLast? ' hidden ' : isSecondLast? `${res.length % 2 == 0? ` md:hidden ` :
                     res.length % 3 == 0? ` lg:hidden `:' '}`: isThirdLast? `${res.length % 3 == 0? ` lg:hidden `: ``}` : ``}">
                    </div>
                    </div>
            `
            booksString += bookString;
        });
        booksCardContainer.innerHTML = booksString;
    
    } catch (error) {
        console.log(error)
    }
}

const handleCategoriesContainerResize = () => {
    const padding = 4 * parseFloat(getComputedStyle(categoriesContainer).fontSize);
    if(categoriesContainer.scrollWidth - padding > categoriesContainer.clientWidth){
        if(categoriesContainer.clientWidth + categoriesContainer.scrollLeft 
        >= categoriesContainer.scrollWidth - padding){
            console.log('SINI 1')
            prevCategoriesButton.style.display = 'flex';
            nextCategoriesButton.style.display = 'none';
        }
        else if(categoriesContainer.scrollLeft === 0){
            console.log('SINI 2')
            prevCategoriesButton.style.display = 'none';
            nextCategoriesButton.style.display = 'flex';
        }
        else{
            console.log('SINI 3')
            prevCategoriesButton.style.display = 'flex';
            nextCategoriesButton.style.display = 'flex';
        }
    }
    else{
        prevCategoriesButton.style.display = 'none';
            nextCategoriesButton.style.display = 'none';
    }
}
nextCategoriesButton.addEventListener('click', () => {
// Menggeser scroll ke kanan
categoriesContainer.scrollLeft += 450; // Sesuaikan dengan jumlah pixel yang Anda inginkan
});

categoriesContainer.addEventListener("touchstart", (e)=> {
    startX = e.touches[0].clientX;
})
categoriesContainer.addEventListener("touchend", (e)=> {
    endX = e.changedTouches[0].clientX;
    const deltaX = startX - endX;
    if(deltaX > 2){
        categoriesContainer.scrollLeft += deltaX
    }
    else if(deltaX < -2){
        categoriesContainer.scrollLeft += deltaX
    }
})

const toggleBooksDropdown = () => {
    const currentMode = mode();
    if(currentMode == 'MOBILE' || currentMode == 'MEDIUM'){
        if(isBooksDropdownMobileOpen){
            closeBooksDropdown()
        }
        else{
            openBooksDropdown()
        }
    }
    else {
        if(isBooksDropdownOpen){
            closeBooksDropdown()
        }
        else {
            openBooksDropdown()
        }
    }
}

// Menambahkan event listener pada tombol "prev" (kiri)
prevCategoriesButton.addEventListener('click', () => {
    // Menggeser scroll ke kiri
categoriesContainer.scrollLeft -= 450; // Sesuaikan dengan jumlah pixel yang Anda inginkan
});
categoriesContainer.addEventListener("scroll", handleCategoriesContainerResize);
window.addEventListener("resize", handleCategoriesContainerResize);
window.addEventListener("DOMContentLoaded", handleCategoriesContainerResize)

const addEventListenerToCategoryButton = (cmap) => {
    for(let[key,value] of cmap){
        const category = key
        const id = category + "-books-btn";
        const element = document.getElementById(id);
        element.addEventListener('click', ()=>{
            setSelectedCategory(category);
        })
    }
}

const setSelectedCategory = (category) => {
    const lastSelectedCategoryElement = document.getElementById(currentSelectedCategory+'-books-btn');
    const nextSelectedCategoryElement = document.getElementById(category+'-books-btn');
    
    if(lastSelectedCategoryElement){
        lastSelectedCategoryElement.classList.remove('border-b-2')
        lastSelectedCategoryElement.classList.remove('border-black')
    }
    if(nextSelectedCategoryElement){
        nextSelectedCategoryElement.classList.add('border-b-2')
        nextSelectedCategoryElement.classList.add('border-black')
    }
    currentSelectedCategory = category;
    setBooksPreference()
    if(booksCardContainerHeader){
        booksCardContainerHeader.textContent = `${category} (${currentfilterBooks.length})`
    }
    console.log('hello')
    window.scrollTo({ top: 0, behavior: "smooth" });
    console.log('AKU PASTIKAN SET SELECTED CATEGORY AMAN')
}

const setCategoriesBar = (categoriesData) => {
    const categoriesContainer = document.getElementById('categories-container');
    let innerHTML = ``;
    for(let[key,value] of categoriesData){
        category = key
        const sanitizedCategory = `${category}`; 
        const categoryHTML = `<div onclick='' id="${sanitizedCategory}-books-btn" class="py-1 mr-4 text-black text-xs ${currentSelectedCategory === sanitizedCategory ? 'border-b-2 border-black' : ''} ">${category}</div>`;
        innerHTML += categoryHTML
    }
    categoriesContainer.innerHTML = innerHTML;
    handleCategoriesContainerResize()
    addEventListenerToCategoryButton(categoriesData)
}

const setCategorySearchList = () => {
    try {
        let innerHTML = ``
        for(let [key,val] of categoryMap){
        const  htmlString = `
        <div  data-value="${key}" name="book-dropdown-values-${key}" class=" block w-full px-4 py-2 hover:bg-indigo-800 " >${key}</div>`;
        innerHTML += htmlString;
        booksDropdownKey.push(key)
    }
    
    bookDropdownValues.forEach((bookDropdownValue)=>{
        bookDropdownValue.innerHTML = innerHTML;
    })
    
    for(let [key,val] of categoryMap){
        const selector = "book-dropdown-values-"+key;
        const buttons = document.getElementsByName(selector);
        console.log(buttons)
        buttons.forEach((btn)=>{
            btn.addEventListener('click', ()=> {
                closeBooksDropdown();
                console.log('hei')
                currentBooksDropdownValuesElement.forEach((ele)=>{
                    ele.textContent = key;
                });
                currentSearchCategory = key
                establishBooksDropdownColor();
            })
        })
        
    }
    } catch (error) {
        console.log(error)
    }
}



const establishBooksDropdownColor = () =>{
    try {
        booksDropdownKey.forEach(key =>{
            const selector = "book-dropdown-values-"+key;
            console.log(selector)
            const elements = document.getElementsByName(selector);
            if(elements.length > 0){
                elements.forEach((element)=>{
                    if(currentSearchCategory == key){
                        element.classList.add("bg-indigo-800")
                    }
                    else{
                        if(element.classList.contains("bg-indigo-800")){
                            element.classList.remove("bg-indigo-800")
                        }
                    }
                })
                
            }
        })
    } catch (error) {
        console.log(error)
    }
}


const getCategories =  () => {
    //console.log('sini')
    sortCategory(currentBooks)
    setCategoriesBar(categoryMap)
}
window.addEventListener("load", async ()=> {
    console.log('--------------');
    console.log(searchText)
    console.log('')
    try {
        await getBooks();
        getCategories();
        categoriesOverlay.classList.remove('hidden');
        console.log('INFO B')
        setSelectedCategory('All');
        firstTime = false
        console.log('INFO C')
        setCategorySearchList();
        console.log('INFO 1')
        establishBooksDropdownColor();
        console.log('INFO 2')
        homeContent.classList.remove('hidden');
        loadingSpinner.style.display = 'none';
        handleCategoriesContainerResize();
        console.log(bookDropdownButton)
        console.log(bookDropdownContent)
    } catch (error) {
        console.log('HELLOOO INI ERROR ');
        console.log(error)
        
    }
})