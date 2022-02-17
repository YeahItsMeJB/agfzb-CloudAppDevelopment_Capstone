async function main(params) {
    var Cloudant = require('@cloudant/cloudant');
    
     const cloudant = Cloudant({
         url: params.COUCH_URL,
         plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
     });
 
 
     try {
         let db = cloudant.db.use('dealerships')
         let docList = await db.list({include_docs: true});
         let data = docList.rows.map((doc) => {
             return doc.doc;
         })
         if(params.state) {
            return { "dealerships": data.filter((dealership) => {
                if(dealership.st == params.state)
                    return true;
                else
                    return false;
            }) };
         }
         else {
            return { "dealerships": data };
         }
     } catch (error) {
         return { error: error.description };
     }
 }
