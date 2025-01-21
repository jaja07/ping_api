db = db.getSiblingDB('fastapi'); // Remplacez par le nom de votre base de données

// Création explicite des collections avec options (si nécessaires)
db.createCollection("kine");
db.createCollection("patients");
db.createCollection("consultations");

// Insertion des données pour les kinés
db.kine.insertOne(
  {
    _id: ObjectId("64c3e5c82db9c3c33d56789a"),
    nom: "Dupont",
    prenom: "Jean",
    email: "jean.dupont@example.com",
    mdp: "hashed_password",
    tel: "0123456789",
    adresse: {
        rue:"123 Rue de Paris",
        ville:"Paris",
        code_postal:"75000"
    }
  });

/// Insertion des documents dans la collection patients
db.patients.insertOne(
    {
      _id: ObjectId("64c3e5c82db9c3c33d56789a"),
      kineid: ObjectId("64c3e5c82db9c3c33d56789a"),
      nom: "Doe",
      prenom: "John",
      date_naissance: new Date("1990-01-01"),
      email: "patient@example.com",
      tel: "+123456789",
      adresse: {
        rue: "rue de la paix",
        ville: "Paris",
        code_postal: "75000"
      },
      sexe: "homme",
      carte_vitale: 123456789,
      anamnese: {
        historique_maladie: "maladie",
        motif: "motif",
        antecedents: "antecedents",
        antecedents_familiaux: "antecedents_familiaux"
      },
      morphostatique: {
        taille: 1.80,
        poids: 80,
        lateralite: "droite",
        remarques: "remarques"
      },
      travail: {
        profession: "profession",
        sport: "sport"
      }
    }
  );
  
  // Insertion des documents dans la collection consultations
  db.consultations.insertOne(
    {
      _id: ObjectId("64c3e5c82db9c3c33d56789a"),
      patientid: ObjectId("64c3e5c82db9c3c33d56789a"),
      date_consultation: new Date("2020-10-20"),
      flexion: { active: 45.0, passive: 50.0 },
      extension: { active: 30.0, passive: 40.0 },
      bdk: "Rapport_BDK_complet.pdf"
    }
  );


