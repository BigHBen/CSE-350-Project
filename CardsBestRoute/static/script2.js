//getting all required elements
const searchWrapper2 = document.querySelector(".search2-input")
const inputBox2 = document.querySelectorAll("input")
const suggBox2 = document.querySelector(".autocom-box2")

//if user press any key and release (start searchbox)
inputBox2[1].onkeyup = (e) =>{
    console.log(e.target.value)
    let userData2 = e.target.value; //user entered data
    let emptyArray2 = [];
    if (userData2){
        emptyArray2 = suggestions.filter((data)=>{
            //filtering array value and user char to lowercase and return only those word
            //sent which starts w/ user entered word
            return data.toLocaleLowerCase().startsWith(userData2.toLocaleLowerCase());
        })
        //console.log(emptyArray2);
        emptyArray2 = emptyArray2.map((data)=>{
            return data = '<li>'+ data +'</li>';
        })
        emptyArray2 = emptyArray2.slice(0,5); //Limit suggestion count to 5
        console.log(emptyArray2);
        searchWrapper2.classList.add('active'); //show autocomplete box
        showSuggestions2(emptyArray2)
        let allList = suggBox2.querySelectorAll("li");
        for (let i = 0; i < allList.length; i++) {
            //adding onclick attribute in all li tag
            allList[i].setAttribute("onclick", "select2(this)");
        }
    }else{
        searchWrapper2.classList.remove('active'); //hide autocomplete box
    }
}

function select2(element){
    let selectuserData2 = element.textContent;
    inputBox2[1].value = selectuserData2; //passing the user selected list item data in textfield
    searchWrapper2.classList.remove('active'); //hide autocomplete box
    //console.log(selectuserData2)
}
function showSuggestions2(list){
    let listData;
    if(!list.length){
        userValue = inputBox2[1].value;
        listData = '<li>' + userValue + '</li>';
    }else{
        listData = list.join('');
    }
    suggBox2.innerHTML = listData;
}


