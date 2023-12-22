function onChangeBFC($event){
    console.log($event.srcElement.value)
    var select_is_safety = document.getElementById("select_is_safety");
    var select_is_obvious = document.getElementById("select_is_obvious");
    if($event.srcElement.value == "true"){
        select_is_safety.classList.remove("disabled");
        select_is_obvious.classList.remove("disabled");
    }else{
        select_is_safety.classList.add("disabled");
        select_is_obvious.classList.add("disabled");
    }
}

function onChangeIsSafety($event){
    var select_safety_type = document.getElementById("select_safety_type");
    if($event.srcElement.value == "true"){
        select_safety_type.classList.remove("disabled");
    }else{
        select_safety_type.classList.add("disabled");
    }
}

function onClickLink(){
    document.getElementById("link_visited").checked = true;
}

$('.ui.accordion').accordion();
//$('.ui.dropdown').dropdown();

// INIT Popups

$('#isBFC').popup({ 
    title: "Bug-fixing commit (BFC)",
    content: `
        Any commit that fixes a bug introduced in a previous commit.
        A bug is a software fault introduced in a certain commit.
    `
});

$('#isOB').popup({ 
    title: "BFC of an obvious bug",
    content: `
    Any commit that fixes a bug
    which  is clearly detectable by usual testing, that is, which causes
    obvious misbehavior on every operation, or so frequently that the
    effects would be clearly noticeable during testing.
    `
});

$('#isSRB').popup({ 
    title:"Safety-related BFC",
    content: `
        Any commit that fixes a safety-related bug.
        A safety-related bug is any bug with potential to affect
        safety-relevant behaviors, as indicated by the categorizations
        described below, even when it may not be detected by typical testing
        because occurrence is intermittent and/or rare.
    
    `
});