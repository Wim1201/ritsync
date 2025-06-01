document.addEventListener("DOMContentLoaded", function () {
    const downloadBtn = document.getElementById("downloadBtn");

    downloadBtn.addEventListener("click", function () {
        const data = {
            thuisadres: "Dr. Kuyperstraat 5, Dongen, Nederland",
            kantooradres: "Kantoorstraat 1, Dongen, Nederland",
            adressen: [
                { adres: "Paleisring 5, Tilburg, Nederland", type: "zakelijk" },
                { adres: "Stationsstraat 20, Breda, Nederland", type: "privé" },
                { adres: "Nieuwstraat 3, Goirle, Nederland", type: "zakelijk" }
            ]
        };

        fetch("/download", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) throw new Error("Download mislukt");
            return response.blob();
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "ritregistratie.pdf";
            document.body.appendChild(a);
            a.click();
            a.remove();
        })
        .catch(error => {
            alert("Er ging iets mis bij het genereren van de PDF.");
            console.error(error);
        });
    });
});
