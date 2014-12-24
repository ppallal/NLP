function putContext(newSentence,ner){ //newSentence->string , ner->OldSentence [('tag','word'),('tag','word'),('tag','word')]
	if (pos = newSentence.search("it")){
		return newSentence.replace("it",getPhoneName(ner));
	}
}

function getPhoneName(tags){
	if(localStorage.getItem("phone")){
		return localStorage.getItem("phone");
	}else{
		//check previous sentence
		retString = "";
		for(i<0;i<tags.length;i++){
			tag = tags[i][0];
			word = tags[i][1];
			mylen = 0;
			if(tag == 'Org'){
				retString += word;
				for(j=i+1;j<tags.length;j++){
					if(tags[j][0] == 'Family' or tags[j][0] == 'Version')
							retString= " " +tags[j][1];
					else{
						break;
					}
				}
			}
		}
		console.log(retString);
		return retString;
	}
}