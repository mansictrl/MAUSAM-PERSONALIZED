import {
    initializeApp
} from "https://www.gstatic.com/firebasejs/12.8.0/firebase-app.js";

import {
    getAuth
} from "https://www.gstatic.com/firebasejs/12.8.0/firebase-auth.js";

import {
    getFirestore
} from "https://www.gstatic.com/firebasejs/12.8.0/firebase-firestore.js";


const firebaseConfig = {
   apiKey: "AIzaSyCFhckMFiEnmAOV1SN_-43VI3L89mmamBY",
  authDomain: "mausam-personalized.firebaseapp.com",
  projectId: "mausam-personalized",
  storageBucket: "mausam-personalized.firebasestorage.app",
  messagingSenderId: "904677310775",
  appId: "1:904677310775:web:278e3b0e43910382a11ab2",
  measurementId: "G-23LGS0L00D"
};


const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);

export const db = getFirestore(app);