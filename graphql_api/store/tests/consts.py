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

ALL_PRODUCTS_QUERY = \
'''
query allProducts {
   allProducts{
    edges {
        node {
            id
            title
        }
    }
   }
}
'''

PRODUCT_QUERY = \
'''
query product($productId: ID!) {
    product(productId: $productId) {
        id
        title
    }
}
'''

CREATE_PRODUCT_MUTATION = \
'''
mutation createProduct($collectionId: ID!, $title: String!, $slug: String!, $inventory: Int!, $promotions: [Int!], $unitPrice: Decimal!){
  createProduct(collectionId: $collectionId, slug: $slug, title: $title, inventory: $inventory, promotions: $promotions, unitPrice: $unitPrice) {
    product {
      id
      title
      unitPrice
      collection {
        id
      }
      promotions {
        edges {
          node {
            id
          }
        }
      }
    }
  }
}
'''

EDIT_PRODUCT_MUTATION = \
'''
mutation editProduct($productId: ID!, $collectionId: ID!, $title: String!, $slug: String!, $inventory: Int!, $promotions: [Int!], $unitPrice: Decimal!){
  editProduct(productId: $productId, collectionId: $collectionId, slug: $slug, title: $title, inventory: $inventory, promotions: $promotions, unitPrice: $unitPrice) {
    product {
      id
      title
      unitPrice
      collection {
        id
      }
      promotions {
        edges {
          node {
            id
          }
        }
      }
    }
  }
}
'''

DELETE_PRODUCT_MUTATION = \
'''
mutation deleteProduct($productId: ID!){
  deleteProduct(productId: $productId){
    ok
  }
}
'''

DELETE_PRODUCT_PROMOTIONS_MUTATION = \
'''
mutation deleteProductPromotions($productId: ID!){
  deleteProductPromotions(productId: $productId){
    ok
  }
}
'''

ALL_PROMOTIONS_QUERY = \
'''
query allPromotions{
  allPromotions {
    edges {
      node {
        id
        description
        discount
      }
    }
  }
}
'''

PROMOTION_QUERY = \
'''
query promotion($promotionId: ID!) {
  promotion(promotionId: $promotionId) {
    id
    description
    discount
  }
}
'''

CREATE_PROMOTION_MUTATION = \
'''
mutation createPromotion($description: String!, $discount: Float!){
  createPromotion(description: $description, discount: $discount){
    promotion {
      id
      description
      discount
    }
  }
}
'''

UPDATE_PROMOTION_MUTATION = \
'''
mutation editPromotion($promotionId: ID!, $description: String, $discount: Float){
  editPromotion(promotionId: $promotionId,description: $description, discount: $discount){
    promotion {
      id
      description
    }
  }
}
'''

DELETE_PROMOTION_MUTATION = \
'''
mutation deletePromotion($promotionId: ID!){
  deletePromotion(promotionId: $promotionId){
    ok
  }
}
'''
