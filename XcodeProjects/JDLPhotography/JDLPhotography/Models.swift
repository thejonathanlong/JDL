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
		case photoThumbnailData = "photoThumbnailData"
	}
	
	let dateCreated : String
	
	let favorite : Int
	
	let photoDestination : String
	
	let image : UIImage?
	
	let thumbnailImage : UIImage?
	
	init(model : Dictionary<String, Any>) {
		dateCreated = model[PhotoAPIKeys.dateCreated.rawValue] as! String
		favorite = model[PhotoAPIKeys.favorite.rawValue] as! Int
		photoDestination = model[PhotoAPIKeys.photoDestination.rawValue] as! String
		
		var image : UIImage? = nil
		if let rawPhoto = model[PhotoAPIKeys.photoData.rawValue] as? String, let photoData = Data(base64Encoded: rawPhoto) {
			image = UIImage(data: photoData)
		}
		self.image = image
		
		var thumbnailImage : UIImage? = nil
		if let rawThumbnailPhoto = model[PhotoAPIKeys.photoThumbnailData.rawValue] as? String, let thumbnailData = Data(base64Encoded: rawThumbnailPhoto) {
			thumbnailImage = UIImage(data: thumbnailData)
		}
		self.thumbnailImage = thumbnailImage
	}
}
