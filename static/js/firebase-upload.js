
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.5.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.5.0/firebase-analytics.js";
import { getStorage, ref, uploadBytes, getDownloadURL } from "https://www.gstatic.com/firebasejs/10.5.0/firebase-storage.js";
const UPLOAD_BUTTONS = [{
    buttonId: 'upload-file-button-example',
    inputId: 'upload-file-example'
    },
]
/*  TODO: tambahkan fungsionalitas lain: seperti menyimpan url ke list
sementara untuk kemudian ditampilkan ke html atau memodifikasi fungsi yang sudah ada */
/*  pertama daftarkan id elemen button dan input kamu dalam suatu dictionary yang 
kemudian dimasukkan ke list UPLOAD_BUTTONS.
cara menggunakannya adalah dengan  memasukkan
<script type="module" src="{% static 'js/firebase-upload.js' %}"></script> 
ke template html kamu.
-isa citra
*/
window.addEventListener('DOMContentLoaded', ()=>{
    UPLOAD_BUTTONS.forEach((elements)=>{
        const element = document.getElementById(elements.buttonId);
        if(element){
            element.addEventListener('click', ()=>{
                uploadImageByElement(elements.inputId);
            })
        }
    })
})
const firebaseConfig = {
    apiKey: "AIzaSyC_SfzhQZo261Z3kBvxNEz2zY1gzKAQ274",
    authDomain: "isa-citra-1691878861005.firebaseapp.com",
    projectId: "isa-citra-1691878861005",
    storageBucket: "isa-citra-1691878861005.appspot.com",
    messagingSenderId: "162707233969",
    appId: "1:162707233969:web:04d90b8885ba8768999690",
    measurementId: "G-ERVNNYPQ3L"
};

  // Initialize Firebase
  const app = initializeApp(firebaseConfig);
  const analytics = getAnalytics(app);
  const storage = getStorage(app);

  /* 
  file ekuivalen dengan event.files[0]
  */
  const uploadImageByElement = async (elementId)=> {
    const ele = document.getElementById(elementId);
    const file = ele?.files[0];
    if(!file){
        console.log("Tidak ada file yang diupload");
        return;
    }
    const storageRef  = ref(storage, "django-image/", file.name);
    try {
        const snapshot = await uploadBytes(storageRef, file);
        const downloadURL = await getDownloadURL(storageRef);
        console.log(downloadURL)
        return downloadURL;
    } catch (error) {
        console.error("Kesalahan dalam mengupload file: ", error)
    }
  }
  const uploadImageByFile = async (file) => {
    const storageRef  = ref(storage, "django-image/", file.name);
    if(!file){
        console.log("Tidak ada file yang diupload");
        return null;
    }
    try {
        const snapshot = await uploadBytes(storageRef, file);
        const downloadURL = await getDownloadURL(storageRef);
        console.log(downloadURL)
        return downloadURL;
    } catch (error) {
        console.error("Kesalahan dalam mengupload file: ", error)
    }
  }


