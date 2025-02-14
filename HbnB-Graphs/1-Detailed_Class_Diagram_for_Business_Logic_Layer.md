classDiagram
class User {
    +UUID id
    +string firstName
    +string lastName
    +string email
    +string password
    +bool isAdmin
    +datetime createdAt
    +datetime updatedAt
    +updateProfile()
    +deleteUser()
}

class Place {
    +UUID id
    +string title
    +string description
    +float price
    +float latitude
    +float longitude
    +User owner
    +list~Amenity~ amenities
    +datetime createdAt
    +datetime updatedAt
    +createPlace()
    +updatePlace()
    +deletePlace()
}

class Review {
    +UUID id
    +User user
    +Place place
    +int rating
    +string comment
    +datetime createdAt
    +datetime updatedAt
    +createReview()
    +updateReview()
    +deleteReview()
}

class Amenity {
    +UUID id
    +string name
    +string description
    +datetime createdAt
    +datetime updatedAt
    +createAmenity()
    +updateAmenity()
    +deleteAmenity()
}

User "1" --> "*" Place : owns
User "1" --> "*" Review : writes
Place "1" --> "*" Review : receives
Place "*" --> "*" Amenity : has

