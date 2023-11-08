//getting all required elements
const searchWrapper = document.querySelector(".search-input")
const inputBox = document.querySelectorAll("input")
const suggBox = document.querySelector(".autocom-box")

//if user press any key and release (start searchbox)
inputBox[0].onkeyup = (e) =>{
    //console.log(e.target.value)
    let userData = e.target.value; //user entered data
    let emptyArray = [];
    if (userData){
        emptyArray = suggestions.filter((data)=>{
            //filtering array value and user char to lowercase and return only those word
            //sent which starts w/ user entered word
            return data.toLocaleLowerCase().startsWith(userData.toLocaleLowerCase());
        })
        //console.log(emptyArray);
        emptyArray = emptyArray.map((data)=>{
            return data = '<li>'+ data +'</li>';
        })
        emptyArray = emptyArray.slice(0,5); //Limit suggestion count to 5
        console.log(emptyArray);
        searchWrapper.classList.add('active'); //show autocomplete box
        showSuggestions(emptyArray)
        let allList = suggBox.querySelectorAll("li");
        for (let i = 0; i < allList.length; i++) {
            //adding onclick attribute in all li tag
            allList[i].setAttribute("onclick", "select(this)");
        }
    }else{
        searchWrapper.classList.remove('active'); //hide autocomplete box
    }
}

function select(element){
    let selectUserData = element.textContent;
    inputBox[0].value = selectUserData; //passing the user selected list item data in textfield
    searchWrapper.classList.remove('active'); //hide autocomplete box
    //console.log(selectUserData)
}
function showSuggestions(list){
    let listData;
    if(!list.length){
        userValue = inputBox[0].value;
        listData = '<li>' + userValue + '</li>';
    }else{
        listData = list.join('');
    }
    suggBox.innerHTML = listData;
}


