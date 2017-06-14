//
//  Models.swift
//  JDLPhotography
//
//  Created by Jonathan Long on 6/3/17.
//  Copyright © 2017 jonathanlong. All rights reserved.
//

import UIKit

protocol BHModel {
	init(model : Dictionary<String, Any>)
}

struct Photo : BHModel{
	
	enum PhotoAPIKeys: String {
		case root = "photos"
		case dateCreated = "dateCreated"
		case favorite = "favorite"
		case photoDestination = "photoDestination"
		case photoData = "photoData"
	}
	
	let dateCreated : String
	
	let favorite : Int
	
	let photoDestination : String
	
	let image : UIImage?
	
	init(model : Dictionary<String, Any>) {
		dateCreated = model[PhotoAPIKeys.dateCreated.rawValue] as! String
		favorite = model[PhotoAPIKeys.favorite.rawValue] as! Int
		photoDestination = model[PhotoAPIKeys.photoDestination.rawValue] as! String
		var image : UIImage? = nil
		if let photoData = Data(base64Encoded: model[PhotoAPIKeys.photoData.rawValue] as! String) {
			image = UIImage(data: photoData)
		}
		self.image = image
	}
}
