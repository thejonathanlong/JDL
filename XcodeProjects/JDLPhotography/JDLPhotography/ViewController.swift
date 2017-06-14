//
//  ViewController.swift
//  JDLPhotography
//
//  Created by Jonathan Long on 6/2/17.
//  Copyright © 2017 jonathanlong. All rights reserved.
//

import UIKit

var photosObserver = 1234

class ViewController: UIViewController {
	
	@IBOutlet weak var imageView: UIImageView!
	
	let dataManager = BigHeroDataManager()
	
	override func viewDidLoad() {
		super.viewDidLoad()
		dataManager.downloadPhotos { (photos) in
			DispatchQueue.main.async {
				self.imageView.image = photos.first?.thumbnailImage
				print("Image size: (\(String(describing: self.imageView.image?.size.width)), \(String(describing: self.imageView.image?.size.height)))");
			}
		}
	}

}

