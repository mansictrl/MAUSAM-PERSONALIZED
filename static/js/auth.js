import {
    createUserWithEmailAndPassword,
    updateProfile
} from "https://www.gstatic.com/firebasejs/12.8.0/firebase-auth.js";

import {
    doc,
    setDoc
} from "https://www.gstatic.com/firebasejs/12.8.0/firebase-firestore.js";

import {
    auth,
    db
} from "./firebase.js";


const signupForm =
    document.getElementById("signup-form");


if (signupForm) {

    signupForm.addEventListener(
        "submit",
        async (event) => {

            event.preventDefault();


            const name =
                document
                    .getElementById("name")
                    .value
                    .trim();


            const email =
                document
                    .getElementById("email")
                    .value
                    .trim();


            const password =
                document
                    .getElementById("password")
                    .value;


            try {

                // =========================
                // CREATE FIREBASE ACCOUNT
                // =========================

                const userCredential =
                    await createUserWithEmailAndPassword(
                        auth,
                        email,
                        password
                    );


                const user =
                    userCredential.user;


                console.log(
                    "New Firebase user:",
                    user.uid
                );


                // =========================
                // SAVE DISPLAY NAME
                // =========================

                await updateProfile(
                    user,
                    {
                        displayName: name
                    }
                );


                // =========================
                // CREATE FIRESTORE PROFILE
                // =========================

                await setDoc(
                    doc(
                        db,
                        "users",
                        user.uid
                    ),
                    {
                        name: name,
                        email: email,
                        interests: [],
                        location: null,
                        activities: [],
                        savedDestinations: [],
                        createdAt: new Date()
                    }
                );


                console.log(
                    "Firestore profile created:",
                    user.uid
                );


                // =========================
                // GET NEW USER ID TOKEN
                // =========================

                const idToken =
                    await user.getIdToken(
                        true
                    );


                console.log(
                    "New user ID token obtained"
                );


                // =========================
                // UPDATE FLASK SESSION
                // =========================

                const response =
                    await fetch(
                        "/auth/login",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                idToken: idToken
                            })
                        }
                    );


                const result =
                    await response.json();


                if (
                    !response.ok ||
                    !result.success
                ) {

                    throw new Error(
                        result.error ||
                        "Could not create Flask session"
                    );

                }


                console.log(
                    "Flask session updated for:",
                    user.uid
                );


                // =========================
                // CONTINUE ONBOARDING
                // =========================

                window.location.href =
                    "/preferences";


            } catch (error) {

                console.error(
                    "Registration error:",
                    error
                );


                alert(
                    error.message
                );

            }

        }
    );

}