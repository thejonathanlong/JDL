//
//  BigHeroDataManager.swift
//  JDLPhotography
//
//  Created by Jonathan Long on 6/2/17.
//  Copyright © 2017 jonathanlong. All rights reserved.
//

import UIKit

typealias BigHeroDataManagerPhotoCompletion = ([Photo]) -> Void

class BigHeroDataManager: NSObject {
	
	static let baseURL = URL(string: "http://127.0.0.1:5000/api/v1")!
	
	var networkDataManager = NetworkDataManager(url: BigHeroDataManager.baseURL)
	
	func downloadPhotos(completion: @escaping BigHeroDataManagerPhotoCompletion) {
		networkDataManager.performRequest(.get, endpoint: "photos") { (data, response) in
			do {
				let photos = try self.serialize(data: data, for: self.rootKey(for: response))
				// ! because if hese are not Photo... big problem...
				completion(photos as! [Photo])
			}
			catch let e {
				print("There was an error serializing the data \(e)")
			}
			
		}
	}

	// MARK - Helpers
	func rootKey(for response: URLResponse) -> String{
		var rootKey = ""
		if let responseURL = response.url {
			switch responseURL.lastPathComponent {
				case "photos":
					rootKey = Photo.PhotoAPIKeys.root.rawValue
					break
				default:
					break
			}
		}
		return rootKey
	}
	
	func serialize(data : Data, for rootKey : String) throws -> [BHModel] {
		var newResponseObjects : [BHModel] = []
		
		let jsonObject = try JSONSerialization.jsonObject(with: data, options: .allowFragments)
		
		if let jsonDict = jsonObject as? Dictionary<String, Any>, let collection = jsonDict[rootKey] as? Array<Dictionary<String, Any>> {
				for item in collection {
					switch rootKey {
						case Photo.PhotoAPIKeys.root.rawValue:
							newResponseObjects.append(Photo(model: item))
							break
						default:
							break
					}
				}
		}
		
		return newResponseObjects
	}
	
}
