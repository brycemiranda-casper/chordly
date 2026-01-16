const NOTES = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"];

let steps = 0;
let original = null;

function transpose(step) {
    const sheet = document.getElementById("chordSheet");

    if (!original) original = sheet.innerText;
    steps += step;

    sheet.innerText = original.replace(
        /\b([A-G])(#{0,1})(m|maj7|maj|min7|min|7|sus4|sus2|dim|aug)?\b/g,
        (m, n, s, suf) => {
            let i = NOTES.indexOf(n + s);
            if (i === -1) return m;
            return NOTES[(i + steps + 12) % 12] + (suf || "");
        }
    );
}
