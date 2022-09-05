COLLECTION_QUERY =  \
'''
query collections($id: Float){
    collections(id: $id) {
        edges {
            node {
            id
            title
            }
        }
    }
}
'''

CREATE_COLLECTION_MUTATION = \
'''
mutation createCollection($title: String!, $featuredProductId: ID){
    createCollection(title: $title, featuredProductId: $featuredProductId) {
 		collection {
            id
            title
            featuredProduct {
                title
                unitPrice
            }
        }
    }
}
'''

EDIT_COLLECTION_MUTATION = \
'''
mutation editCollection($collectionId: ID!, $title: String!){
    editCollection(collectionId: $collectionId, title: $title) {
 		collection {
            id
            title
            featuredProduct {
                title
                unitPrice
            }
        }
    }
}
'''

DELETE_COLLECTION_MUTATION = \
'''
mutation deleteCollection($collectionId: ID!) {
    deleteCollection(collectionId: $collectionId) {
        ok
    }
}
'''