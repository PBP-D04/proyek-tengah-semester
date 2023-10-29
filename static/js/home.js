//let currentUser = {{user|default:"null"}}
var currentBooks = [];
let carouselBooks = [];
const carousel = document.getElementById("carousel");
const prevButton = document.getElementById("prev");
const nextButton = document.getElementById("next");
let currentIndex = 0;
let indicators = null;
const dropdownButton = document.getElementById("dropdownDelayButton");
const dropdownCurrentText = document.getElementById("dropdownButtonText")
const dropdownContent = document.getElementById("dropdownDelay");
const dropdownButtonsContent = dropdownContent.querySelectorAll("button");
const dropdownIcon = document.getElementById("homeDropdownIcon");
const homeContent = document.getElementById("homeContent");

let userId = document.getElementById('user-id').getAttribute('data-user-id');
let username = document.getElementById('user-username').getAttribute('data-user-username');

console.log(userId,username)

const carouselButtonContainer = document.getElementById("carousel-button-container");
const carouselContainer = document.getElementById("carousel-container");
const topDivider = document.getElementById('top-divider');
const bottomDivider = document.getElementById('bottom-divider');
const allBooksButton = document.getElementById('all-books-button');
let preferences = {
    'sortBy': 'Terbaru'
}

// current search category
let sCurrentSearchCategory = 'All'

// track mode lebar layar sekarang
let mode = (width) => width < 768 ? 'MOBILE' : width < 1024? 'MEDIUM' : 'LARGE';
let prevWidth = window.innerWidth;

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
    console.log('search-url: ', searchText)
    const searchUrl = `/search-books/${sCurrentSearchCategory}/${searchText}`;
    window.location.href = searchUrl;

}

pcSearchAnswerBtn.addEventListener('click', ()=> {
    validateSearch()
})
mobileSearchAnswerBtn.addEventListener('click', ()=> {
    validateSearch()
})

/*Search Dropdown*/
let isSearchDropdownMobileOpen = false;
let isSearchDropdownOpen = false;
const searchDropdownButton = document.querySelectorAll('.dropdown-button-xl');
const searchCurrentDropdownValue = document.querySelectorAll('.books-dropdown-current-value');
const searchDropdownSVG = document.querySelectorAll('.books-dropdown-svg');
const searchDropdownContent = document.querySelectorAll('.books-dropdown-content');
const searchDropdownValue = document.querySelectorAll('.books-dropdown-values');
const searchDropdownKey = [];



// map untuk categories
let categoryMap = new Map();

const MAX_HOMEPAGEBOOKS = 12;
var currentValue = 'Terbaru';
var isDropdownOpen = false;
const NO_THUMBNAIL_URL = 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/495px-No-Image-Placeholder.svg.png?20200912122019'


searchDropdownButton.forEach((btn)=> {
    btn.addEventListener('click', ()=> {
        console.log('URAAAAAAA')
        try {
            toggleSearchDropdown()
        } catch (error) {
            console.log('ADA ERROR OH TIDAK BAGAIMANA INIII????')
        }
    })
})

//SUDAH SESUAI
const setSearchCategoryList = () =>{
  console.log('ULALA...')
  let innerHTML = ``;
  try {
    for(let[key,val] of categoryMap){
        const htmlString = 
        `<div  data-value="${key}" name="book-dropdown-values-${key}" class=" block w-full px-4 py-2 hover:bg-indigo-800" >${key}</div>`;
        innerHTML += htmlString;
        searchDropdownKey.push(key);
    }
    searchDropdownValue.forEach((element)=>{
        element.innerHTML = innerHTML;
    });
    for(let[key,val] of categoryMap){
        const selector = "book-dropdown-values-"+key;
        const buttons = document.getElementsByName(selector);
        buttons.forEach((btn)=>{
            btn.addEventListener('click', ()=> {
                closeSearchDropdown();
                searchCurrentDropdownValue.forEach((ele)=>{
                    ele.textContent = key;
                })
                sCurrentSearchCategory = key;
                establishSearchDropdownColor();
            })
        })
    }
  }
  catch(error){
    console.log(error)
  }
}

// SUDAH SESUAI
const establishSearchDropdownColor = () =>{
    console.log(sCurrentSearchCategory)
    try {
        searchDropdownKey.forEach(key =>{
            const selector = "book-dropdown-values-"+key;
            console.log('ini selector: ',selector)
            const elements = document.getElementsByName(selector);
            if(elements.length > 0){
                elements.forEach((element)=>{
                    if(sCurrentSearchCategory == key){
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

const toggleSearchDropdown = () => {
    const currentMode = mode(window.innerWidth)
    if(currentMode == 'MOBILE' || currentMode == 'MEDIUM'){
        if(isSearchDropdownMobileOpen){
            closeSearchDropdown()
        }
        else{
            openSearchDropdown()
        }
    }
    else {
        if(isSearchDropdownOpen){
            closeSearchDropdown()
        }
        else {
            openSearchDropdown()
        }
    }
}

// buka dropdown
const openSearchDropdown = () => {
    console.log('INFOKAN KETERBUKAAN')
    console.log(searchDropdownContent)
    const currentMode = mode(window.innerWidth)
    try {
        if(currentMode == 'MOBILE' || currentMode == 'MEDIUM'){
            searchDropdownContent[1].className = `max-h-[24rem] absolute top-14 left-0 z-20  bg-violet-950 divide-y divide-gray-100 rounded-lg shadow w-44 `
            isSearchDropdownMobileOpen = true;
        }
        else{
            searchDropdownContent[0].className = `max-h-[24rem] absolute top-14 right-0 z-20  bg-violet-950 divide-y divide-gray-100 rounded-lg shadow w-44`
            isSearchDropdownOpen = true;
        }
        
        searchDropdownSVG.forEach(svg => {
            svg.classList.add('rotate-180');
            console.log("APA SIHHHHHHHHHHH KENAPA ")
        });
        console.log(searchDropdownSVG);
    } catch (error) {
        console.log(error)
    }
}

// tutup
const closeSearchDropdown = () => {
    console.log('INFOKAN KETERTUTUPAN')
    const currentMode = mode(window.innerWidth)
    if(currentMode == 'MOBILE' || currentMode == 'MEDIUM'){
        searchDropdownContent[1].className = `max-h-[24rem] hidden absolute top-12 right-0 z-20  bg-violet-700 divide-y divide-gray-100 rounded-lg shadow w-44 `
        isSearchDropdownMobileOpen = false;
    }
    else{
        searchDropdownContent[0].className = `max-h-[24rem] hidden absolute top-12 right-0 z-20  bg-violet-700 divide-y divide-gray-100 rounded-lg shadow w-44`
        isSearchDropdownOpen = false;
    }
    searchDropdownSVG.forEach(svg => {
        svg.classList.remove('rotate-180');
    });
}

const setMode = () => {
    if(mode() == 'MOBILE'){
        searchDropdownContent[0].className = `max-h-[24rem] hidden absolute top-12 right-0 z-20  bg-violet-700 divide-y divide-gray-100 rounded-lg shadow w-44 `;
        searchDropdownSVG[0].classList.remove('rotate-180');
        isSearchDropdownOpen = false;
    }
    else{
        searchDropdownContent[1].className = `max-h-[24rem] hidden absolute top-12 right-0 z-20  bg-violet-700 divide-y divide-gray-100 rounded-lg shadow w-44 `;
        searchDropdownSVG[1].classList.remove('rotate-180');
        isSearchDropdownMobileOpen = false;
    }
}
window.addEventListener('resize',setMode)

window.addEventListener('click', (event)=> {
    console.log('ADA YANG TERCLICK')
    const currentWidth = window.innerWidth;
    const currentMode = mode(currentWidth)
    if(currentMode == 'MOBILE' || currentMode =='MEDIUM'){
        console.log('MOBILE TERCLICK')
        if(! searchDropdownButton[1].contains(event.target)){
            console.log('MAAF AKU INTERUPSI!!!')
            return closeSearchDropdown()
        }
        if( searchDropdownButton[1].contains(event.target)){
            console.log('TERCLICK YOIIII')
        }
        
    }
    else{
        console.log('PC TERCLICK')
        if(! searchDropdownButton[0].contains(event.target)){
            return closeSearchDropdown();
        }
    }
});

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


const getBooks = async ()=>{
    const loading = document.getElementById('loading-text');
    try {
        loading.style.display = 'flex';
        const resJson = await fetch('/get-books/', {
            method:'GET'
        });
        const res = await resJson.json();
        console.log(res);
        const books = res.books;
        books.reverse();
       setCarouselBooks(getRandomElementsFromArray(books, 5));
       //setCarouselBooks([])
        currentBooks = [...books];
       setHomepageBooks(currentBooks);
       sortCategory(books);
        //setHomepageBooks([])
        loading.style.display = 'none';
    } catch (error) {
        loading.style.display = 'none';
    }

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

window.addEventListener("load", ()=>{
    dropdownCurrentText.textContent = currentValue;
    establishDropdownSelectedValueColor();
})

document.addEventListener("click", (event) => {
// Periksa apakah elemen yang diklik adalah dropdownButton
if (event.target !== dropdownContent) {
    // Periksa apakah elemen yang diklik adalah dropdownContent atau elemen dalam dropdownContent
    if (!dropdownContent.contains(event.target)) {
        // Jika bukan dropdownButton, dropdownContent, atau elemen dalam dropdownContent yang diklik, maka tutup dropdownContent
        closeDropdown();
    }
}
});

const sortBooksBy = () => {
    
    const sortBy = preferences.sortBy;
    console.log(sortBy)
    const books = [...currentBooks];
    console.log('ini buku yg asli->', currentBooks.length)

    books.sort((firstBook, secondBook)=> {

        if(sortBy == 'Terbaru'){
            return new Date(secondBook.user_publish_time) - new Date(firstBook.user_publish_time)
        }
        if(sortBy == 'Terlama'){
            return new Date(firstBook.user_publish_time) - new Date(secondBook.user_publish_time)
        }
        if(sortBy == 'Paling Banyak Disukai'){
            return 0;
        }
        if(sortBy == 'Review Terbanyak'){
            return 0;
        }
    });
    console.log('ini buku yang disort->',books.length)
    console.log(currentBooks.slice(0,12))
    console.log(books.slice(0,12))
    setHomepageBooks(books);
}

const establishDropdownSelectedValueColor =  ()=>{
    dropdownButtonsContent.forEach(button => {
        if(button.getAttribute("data-value") != currentValue){
            button.classList.remove("bg-indigo-800");
        }
        else {
            if(!button.classList.contains("bg-indigo-800")){
                button.classList.add("bg-indigo-800")
            }
        }
    })
}

const openDropdown = () => {
    dropdownContent.classList.remove('hidden');
    isDropdownOpen = true;
    dropdownIcon.setAttribute("transform", "scale(1, -1)");
}

const toggleDropdown = () => {
    if(isDropdownOpen){
        closeDropdown()
    }
    else{
        openDropdown()
    }
}

const closeDropdown = () => {
    if(!dropdownContent.classList.contains('hidden')){
        dropdownContent.classList.add('hidden')
    }
    isDropdownOpen = false;
    dropdownIcon.setAttribute("transform", "scale(1, 1)");
}
dropdownButton.addEventListener("click", (event) => {
    toggleDropdown();
    event.stopPropagation();
    
});

dropdownButtonsContent.forEach(button => {
    button.addEventListener("click", ()=>{
        const newValue = button.getAttribute("data-value");
        preferences.sortBy = newValue
        currentValue = newValue;
        dropdownCurrentText.textContent = currentValue;
        establishDropdownSelectedValueColor();
        sortBooksBy()
        closeDropdown();
    })
});


function getRandomElementsFromArray(array, numElements) {
    const newArray = [...array];
    const shuffledArray = newArray.sort(() => 0.5 - Math.random()); // Mengacak urutan array
    return shuffledArray.slice(0, numElements); // Mengambil sejumlah elemen
  }

const likeOrDislikeBook = async (idUser,bookId) => {
    if(!idUser){
        return
    }
    const url = '/like-book-json/'
    console.log(userId,idUser,bookId)
    data = {'userId': idUser, 'bookId':bookId}
    const requestOptions = {
            method: 'POST', 
            headers: {
                'Content-Type': 'application/json', 
            },
            body: JSON.stringify(data), 
        };
    try {
        const resJson = await fetch(url, requestOptions);
        const res = await resJson.json()
        if(res.book){
            updateBooksState(res.book);
        }
    } catch (error) {
        console.log(error)
    }
}

const updateBooksState = (updatedBook) => {
    const bookIndex = currentBooks.findIndex(book => book.id === updatedBook.id);
    if(bookIndex != -1){
        currentBooks[bookIndex] = updatedBook
    }
    setHomepageBooks(currentBooks)
}

const setCarouselBooks = (res) => {
    
    const carousel = document.getElementById('carousel');
    let booksString = '';
    try {
        if(res.length == 0){
            carouselContainer.classList.add('hidden');
            return;
        }
        res.forEach((book, index)=>{
            console.log(book)
            console.log(index)
            const bookString = `<div class="flex w-full h-full justify-center  items-center flex-shrink-0 ">
            <div  class="my-auto">
                <div class=" px-2  flex  min-h-[13rem] max-w-[24rem] md:max-w-[32rem] lg:max-w-[48rem] py-2">
                    <img class=" rounded-md h-[11rem] md:h-[18rem] aspect-[3/4]" src=${book.thumbnail? book.thumbnail : NO_THUMBNAIL_URL } alt="">
                    <div class=" pl-3 flex-1 flex flex-col  ">
                        <div class="flex   justify-between items-start ">
                        <div class="mt-1 mr-2">
                        
                        <a class="font-bold text-sm line-clamp-2 text-[#460C90]" href="detail/book-detail/${book.id}">${ book.title ? book.title : 'No Title' }</a>

                        <h1 class="text-[#C52A62] text-xs line-clamp-2">
                        ${book.authors.length > 0 ? book.authors.map((author,index)=>{
                            if(index == book.authors.length - 1){
                                return `<a>${author}</a><span>.</span>`
                            }
                            return `<a>${author}</a><span>, </span>`
                        }) : 'Unknown'}
                        </h1>
                    </div> 
                            <div class="ml-auto flex flex-col items-center justify-center">
                                <div class=" fas fa-heart ${book.likes.find((user)=> user.userId == userId)? 'text-red-500':'text-gray-300'} text-lg">
                                </div>
                                <h1 class="text-xs">1024</h1>
                            </div>
                        </div>
                        <div class="text-xs text-black mt-1 line-clamp-1">
                            Created by <a href="/profile/${book.username??''}" class="text-[#460C90] hover:underline">${book.fullname? book.fullname :'Unknown'}</a>
                        </div>
                        <div class="mt-1 flex items-center space-x-2">
                            <div class="rating text-yellow-400 text-sm">
                                <span class="fas fa-star"></span>
                                <span class="fas fa-star"></span>
                                <span class="fas fa-star"></span>
                                <span class="fas fa-star"></span>
                                <span class="fas fa-star-half-alt"></span>
                            </div> 
                            <div class="text-xs text-black line-clamp-1">
                                415 Reviews
                            </div>
                        </div>    
                        <div  class="mt-1 text-[#C52A62] text-xs line-clamp-2">
                        ${book.categories.length > 0 ? book.categories.map((category,index)=>{
                            if(index == book.categories.length - 1){
                                return `<a class="hover:underline" href="/search-books/${category}" >${category}</a><span>.</span>`
                            }
                            return `<a class="hover:underline" href="/search-books/${category}">${category}</a><span>, </span>`
                        }) : 'No categories'}
                        </div>
                        <div  class=" text-black text-xs md:text-sm line-clamp-2 md:line-clamp-4">
                            ${book.description? book.description : 'No description'}
                        </div>
                        <div  class="mt-1 text-[#C52A62] font-bold text-sm line-clamp-2">
                        ${book.currencyCode && book.price? `${book.currencyCode} <span>${book.price}</span>` : 'FREE'}
                        </div>
                        <a href="detail/book-detail/${book.id}" class="mt-auto w-full max-w-[16rem] flex items-center justify-center text-xs md:text-sm lg:text-base text-white py-2 rounded-md bg-violet-950 hover:bg-indigo-950">
                            Lihat Detail Buku
                        </a>


                    </div>
                </div>
                </div>
    
          </div>`;
          booksString += bookString;
        });
        carousel.innerHTML = booksString;

        let buttonInnerHTML = ``;
        res.forEach((element, index)=> {
            buttonInnerHTML += `<button id="indicator-${index+1}" class="w-3 h-3 rounded-full bg-gray-400"></button>`
        })
        carouselButtonContainer.innerHTML = buttonInnerHTML;
        const updateIndicators = document.querySelectorAll("[id^='indicator-']");
        indicators = updateIndicators;
        indicators.forEach((indicator, index) => {
            indicator.addEventListener("click", () => {
              currentIndex = index;
              updateCarousel();
            });
            });
        
    } catch (error) {
        console.log(error)
    }
}


function updateCarousel() {
    const translateX = currentIndex * -100;
    carousel.style.transform = `translateX(${translateX}%)`;
    updateIndicators()
  }
function updateIndicators() {
    if(! indicators){
        return;
    }
    indicators.forEach((indicator, index) => {
      if (index === currentIndex) {
        indicator.classList.remove("bg-gray-400");
        indicator.classList.remove("w-3")
        indicator.classList.add("bg-indigo-600");
        indicator.classList.add("w-6")
      } else {
        indicator.classList.remove("bg-indigo-600");
        indicator.classList.remove("w-6")
        indicator.classList.add("bg-gray-400");
        indicator.classList.add("w-3")
      }
    });
  }




const setHomepageBooks = (prevRes) => {
    res = [...prevRes.slice(0, MAX_HOMEPAGEBOOKS)]
    const booksCardContainer = document.getElementById('books-card-container');
    console.log('ini books card container', booksCardContainer);
    let booksString = '';
    if(res.length == 0){
            try {
                booksCardContainer.className = "flex flex-col items-center justify-center px-1 w-full pb-24 grow";
    
                topDivider.classList.add('hidden');
                bottomDivider.classList.add('hidden');
                booksCardContainer.innerHTML = `
                <div class=' min-w-[12rem] w-[15%] h-auto'>
                    <img class='w-full h-full' src="/static/img/empty.svg" >
                </div>
                <div class="text-lg font-bold flex w-full justify-center mt-3">
                Maaf Buku Tidak Ada.
                </div>
                `;
                allBooksButton.classList.add('hidden')
                console.log('SAMPAI SINI')
            } catch (error) {
                console.log(error)
            }

            return;
    }
    try {
        booksCardContainer.className = "grid  md:grid-cols-2 lg:grid-cols-3  gap-y-2 w-full px-1 grid-flow-row auto-rows-max";
        topDivider.classList.remove('hidden');
        bottomDivider.classList.remove('hidden');
        allBooksButton.classList.remove('hidden');
        if(currentBooks.length <= 12){
            allBooksButton.classList.add('hidden')
        }
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
                        
                            <a class="font-bold text-sm line-clamp-2 text-[#460C90]" href="detail/book-detail/${book.id}">${ book.title ? book.title : 'No Title' }</a>
                                
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
                                    <div onclick="likeOrDislikeBook(${userId},${book.id})" class="fas fa-heart ${book.likes.find((user)=> user.userId == userId)? 'text-red-500':'text-gray-300'} text-lg">
                                    </div>
                                    <h1 class="text-xs">${book.likes.length}</h1>
                                </div>
                            </div>
                            
                            <div class="text-xs text-gray-400 mt-1">
                            Created by <a href="/profile/${book.username??''}" class="text-[#460C90] hover:underline">${book.fullname? book.fullname :'Unknown'}</a>
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
                                        return `<a class="hover:underline" href="/search-books/${category}">${category}</a><span>.</span>`
                                    }
                                    return `<a class="hover:underline" href="/search-books/${category}">${category}</a><span>, </span>`
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

window.addEventListener("DOMContentLoaded", async ()=>{
    await getBooks();
    setSearchCategoryList();
    establishSearchDropdownColor();
    updateIndicators();
    nextButton.addEventListener("click", () => {
        currentIndex++;
        if (currentIndex >= indicators.length ?? 0) {
          currentIndex = 0;
        }
        updateCarousel();
      });
    
      carousel.addEventListener("touchstart", (e) => {
      startX = e.touches[0].clientX;
    });
    
    carousel.addEventListener("touchend", (e) => {
      endX = e.changedTouches[0].clientX;
      if (startX - endX > 50) {
        currentIndex++;
        if (currentIndex >= indicators.length ?? 0) {
          currentIndex = 0;
        }
        updateCarousel();
      } else if (endX - startX > 50) {
        currentIndex--;
        if (currentIndex < 0) {
          currentIndex = indicators.length - 1 ?? 0;
        }
        updateCarousel();
      }
    });
    
    prevButton.addEventListener("click", () => {
        currentIndex--;
        if (currentIndex < 0) {
          currentIndex = indicators.length - 1 ?? 0;
        }
        updateCarousel();
      });
    homeContent.classList.remove("hidden");
})