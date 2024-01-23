const { Session } = require('ecoledirecte.js');
const { Indentifiant, MotDePasse } = require('./config.json');
total = 0
nbr = 0

async function note() {
    const session = new Session(Indentifiant, MotDePasse);
    const account = await session.login().catch(err => {
        console.log(err)
    });
    var moyenne = 0
    var NbrNote = 0

    const noteTotal = await account.getGrades();
    var list = noteTotal.length
    if(list != 0){
        var i = 0
        
        while(list > i){
            if(noteTotal[i].periodCode == 'A003' && noteTotal[i]._raw.nonSignificatif == false && noteTotal[i].subjectName == input && noteTotal[i].isLetter == false){
                iNote = noteTotal[i].value
                iNoteSur = noteTotal[i].outOf

                NoteSur20 = (iNote / iNoteSur) * 20
                moyenne = moyenne + NoteSur20
                NbrNote = NbrNote + 1
            }
            i = i + 1
        }
    }

    moyenne = moyenne / NbrNote

    console.log(moyenne)
    total += moyenne
    nbr += 1
}
async function moyennegg(){
input = 'FRANCAIS'
await note()

input = 'ANGLAIS LV1'
await note()

input = 'ESPAGNOL LV2'
await note()

input = 'HISTOIRE-GEOGRAPHIE'
await note()

input = 'ENS. MORAL & CIVIQUE'
await note()

input = 'ENSEIGN.SCIENTIFIQUE'
await note()

input = 'ED.PHYSIQUE & SPORT.'
await note()

input = 'MATHEMATIQUES'
await note()

input = 'PHYSIQUE-CHIMIE'
await note()

input = 'NUM. SC.INFO. HE'
await note()


moyenneg = total / nbr
console.log('\n', moyenneg)
}

moyennegg()